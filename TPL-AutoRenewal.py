from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Enable waiting
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Each user has a pair of credentials
numUsers = numUsers / 2

userIndex = 0
USERNAME = []
PASSWORD = []

# Read user credentials from external file and add them to arrays
while userIndex < numUsers:
    USERNAME.append(lines[17 + 2 * userIndex])
    PASSWORD.append(lines[18 + 2 * userIndex])
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
    itemIndex = 1

    while renewing:
        itemStatusXPath = "//table[@class='item-list']/tbody[{}]//div[@class='item-status']".format(itemIndex)
        renewButtonXPath = "//table[@class='item-list']/tbody[{}]//button".format(itemIndex)

        # Wait until checkouts page loads
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, itemStatusXPath))
        )
        elem = driver.find_element_by_xpath(itemStatusXPath)
        elemtext = elem.text.lower()

        # If checkout is due today or tomorrow renew hold
        if 'tomorrow' in elemtext or 'today' in elemtext or 'overdue' in elemtext:
            elem = driver.find_element_by_xpath(renewButtonXPath)
            elem.click()
            itemIndex += 1
        else:
            renewing = False

        print(renewing)

    userIndex += 1
