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

totalVotes = 1000
numVotes = 0

while numVotes < totalVotes:
    driver = webdriver.Chrome("chromedriver.exe")
    # driver.get("http://www.senorashby.com/march-1-7.html")
    driver.get("http://www.easypolls.net/poll.html?p=5c7c80bee4b064bdfdc5d38a")

    # Find button id
    buttonXPath = "//*[@id='l_0_5c7c80bee4b064bdfdc5d38a']"
    elem = driver.find_element_by_xpath(buttonXPath)
    elem.click()

    # Hit submit button
    buttonXPath = "//*[@id='OPP-poll-vote-button']"
    elem = driver.find_element_by_xpath(buttonXPath)
    elem.click()

    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/table/tbody/tr/td/div/div/div[2]"))
        )
    except TimeoutException:
        renewing = False
        break

    print("Number of votes:", numVotes)
    driver.close()

    numVotes += 1
