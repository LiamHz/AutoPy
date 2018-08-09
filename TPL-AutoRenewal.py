from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Enable waiting
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Enable excpetions
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Enable emailing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

numUsers = 0
searching = True

f = open("AuthenticationCredentials.txt", 'r')
lines = f.read().splitlines()

# Determine how many users are being serviced by this script
while searching:
    try:
        if lines[17 + numUsers] == "":
            searching = False
        else:
            numUsers += 1
    # If there are no more lines in the authentication file
    # Then there are no more user credentials
    except IndexError:
        searching = False

# Each user has a trio of credentials
numUsers = numUsers / 3

userIndex = 0
USERNAME = []
PASSWORD = []

EMAIL_USERNAME = lines[1]
EMAIL_PASSWORD = lines[2]

TOADDR = []

# Read user credentials from external file and add them to arrays
while userIndex < numUsers:
    TOADDR.append(lines[17 + 3 * userIndex])
    USERNAME.append(lines[18 + 3 * userIndex])
    PASSWORD.append(lines[19 + 3 * userIndex])
    userIndex += 1
f.close()

# The current user being serviced
userIndex = 0

while userIndex < numUsers:
    driver = webdriver.Chrome()
    driver.get("https://account.torontopubliclibrary.ca/checkouts")

    # Login to TPL
    elem = driver.find_element_by_id('userID')
    elem.clear()
    elem.send_keys(USERNAME[userIndex])
    elem = driver.find_element_by_id('password')
    elem.send_keys(PASSWORD[userIndex])
    elem.send_keys(Keys.RETURN)

    renewing = True
    itemsRenewed = []
    itemIndex = 1

    while renewing:
        itemTitleXPath = "//table[@class='item-list']/tbody[{}]//div[@class='item-title']".format(itemIndex)
        itemStatusXPath = "//table[@class='item-list']/tbody[{}]//div[@class='item-status']".format(itemIndex)
        renewButtonXPath = "//table[@class='item-list']/tbody[{}]//button".format(itemIndex)

        # Wait until checkouts page loads
        # If itemStatusXPath is not found it's most likely because
        # it's trying to access past the end of the checkout list
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, itemStatusXPath))
            )
        except TimeoutException:
            renewing = False
            break

        elem = driver.find_element_by_xpath(itemStatusXPath)
        elemtext = elem.text.lower()

        # If checkout is due today or tomorrow renew hold
        if 'tomorrow' in elemtext or 'today' in elemtext or 'overdue' in elemtext:

            # Add matching item to list showing renewal has been attempted
            elem = driver.find_element_by_xpath(itemTitleXPath)
            itemsRenewed.append(elem.text)

            # Test if renew button is available
            try:
                elem = driver.find_element_by_xpath(renewButtonXPath)
                elem.click()
            except NoSuchElementException:
                print("No Renew Button!")

            itemIndex += 1
        else:
            renewing = False

    itemsFailedRenewed = []

    # Check if any checkouts failed to renew
    for title in itemsRenewed:
        if title in driver.page_source:
            itemsFailedRenewed.append(title)

    # If any results failed to renew email them to user
    if len(itemsFailedRenewed) >= 1:
        s = "\n"
        formattedItemsFailedRenewed = s.join(itemsFailedRenewed)

        addr = EMAIL_USERNAME
        toaddr = TOADDR[userIndex]
        msg = MIMEMultipart()
        msg['From'] = addr
        msg['To'] = toaddr
        msg['Subject'] = "TPL AutoRenewal: The following items could not be renewed"

        # Allow Unicode characters to be emailed
        text = MIMEText(formattedItemsFailedRenewed.encode('utf-8'), 'plain', 'UTF-8')

        msg.attach(text)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(addr, EMAIL_PASSWORD)
        print("Sent email to {}".format(toaddr))
        server.sendmail(addr, toaddr, msg.as_string())
        server.quit()

    userIndex += 1
