from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Enable waiting
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Read user credentials from external file
f = open("AuthenticationCredentials.txt", 'r')
lines = f.read().splitlines()
USERNAME = lines[17]
PASSWORD = lines[18]

driver = webdriver.Chrome()
driver.get("https://account.torontopubliclibrary.ca/checkouts")
# Login to TPL
elem = driver.find_element_by_id('userID')
elem.clear()
elem.send_keys(USERNAME)
elem = driver.find_element_by_id('password')
elem.send_keys(PASSWORD)
elem.send_keys(Keys.RETURN)
# Wait until checkouts page loads
xxx = "//table[@class='item-list']/tbody[1]/tr[@class='item-row']/td[@class='hidden-mobile']/div[@class='item-due']"
elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xxx))
)
elem = driver.find_element_by_xpath(xxx)
print(elem.text)
