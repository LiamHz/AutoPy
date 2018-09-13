# Renew checkouts from the Toronto Public Library that are due today, tomorrow, or overdue
# If an item could not be renewed, notify the user via email

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

# Enable time delay
import time

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

# Renew checkouts that are due today, tomorrow or overdue
while userIndex < numUsers:

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://account.torontopubliclibrary.ca/checkouts")

    # Login to TPL
    elem = driver.find_element_by_id('userID')
    elem.clear()
    elem.send_keys(USERNAME[userIndex])
    elem = driver.find_element_by_id('password')
    elem.send_keys(PASSWORD[userIndex])
    elem.send_keys(Keys.RETURN)


    # Add books that need to be renewed to a list
    searching = True
    itemsToRenew = []
    itemIndex = 1
    itemsRenewed = {}

    while searching:
        itemTitleXPath = "//table[@class='item-list']//tbody[{}]//tr[2]//td[3]//div[1]/a".format(itemIndex)
        itemStatusXPath = "//table[@class='item-list']//tbody[{}]//tr[2]//td[5]//div[1]".format(itemIndex)
        itemDueDateXPath = "//table[@class='item-list']//tbody[{}]//tr[2]//td[4]//div[1]".format(itemIndex)

        # Wait until checkouts page loads
        # If itemStatusXPath is not found it's most likely because
        # it's trying to access past the end of the checkout list
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, itemStatusXPath))
            )
        except TimeoutException:
            searching = False
            break

        elem = driver.find_element_by_xpath(itemStatusXPath)
        elemtext = elem.text.lower()

        # If checkout is due today, tomorrow, or overdue add book to list to be renewed
        if 'tomorrow' in elemtext or 'today' in elemtext or 'overdue' in elemtext:

            # Add matching item to dict showing renewal has been attempted
            # {k: v} = {Title: Status}
            elemTitle = driver.find_element_by_xpath(itemTitleXPath).text
            elemDueDate = driver.find_element_by_xpath(itemDueDateXPath).text
            itemsRenewed[elemTitle] = elemDueDate

            itemTitle = driver.find_element_by_xpath(itemTitleXPath)
            itemsToRenew.append(itemTitle.text)

            itemIndex += 1
        else:
            searching = False


    # Renew items in list
    for item in itemsToRenew:
        # Find renew button by first locating the item title element
        renewButtonXPath = "//table[@class='item-list']//a[contains(text(), item)]/../../..//tr[2]//td[8]//button[1]"
        try:
            print(item)
            renewButton = driver.find_element_by_xpath(renewButtonXPath)
            renewButton.click()
            time.sleep(3)
        except NoSuchElementException:
            print("No Renew Button for {}!".format(item))


    # If any items failed to renew, add them to itemsFailedRenewed list
    itemsFailedRenewed = []
    itemIndex = 1

    for title, status in itemsRenewed.items():
        itemDueDateXPath = "//table[@class='item-list']//a[contains(text(), item)]/../../..//tr[2]//td[4]//div[1]"
        itemDueDate = driver.find_element_by_xpath(itemDueDateXPath).text

        # If a item's due date is the same as it was before the item failed to renew
        if itemsRenewed[title] == itemDueDate:
            itemsFailedRenewed.append(title)


    # If any results failed to renew email a notification to user
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
