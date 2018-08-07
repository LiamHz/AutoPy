from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Enable waiting
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

desiredSheets = input("What piece do you wish to download? \n")
searchSite = "musescore.com"
firstGoogleResult = '(//h3)[1]/a' #All search results are held in H3s

# Set download location NOT WORKING
options = webdriver.ChromeOptions()
options.add_argument(r"download.default_directory=C:\Users\liamh\Documents\Sheet Music")

driver = webdriver.Chrome(chrome_options=options)
driver.get(("https://www.google.ca/search?&q=site%3A{}+{}").format(searchSite, desiredSheets))

# Wait until google results load
elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, firstGoogleResult))
)

# Go to the first result's log in redirect
redirect = 'user/login?destination=/'
elem = driver.find_element_by_xpath(firstGoogleResult)
link = elem.get_attribute('href')
link = link[:22] + redirect + link[22:]
driver.get(("{}".format(link)))
print(link)

# Signin to Musescore
elem = driver.find_element_by_id('edit-name')
elem.send_keys('liam-hinzman')
elem = driver.find_element_by_id('edit-pass')
elem.send_keys('Shusaku123!')
elem.send_keys(Keys.TAB)
elem.send_keys(Keys.TAB)
elem.send_keys(Keys.RETURN)

# Download as pdf
elem = driver.find_element_by_class_name('js-score-download-status')
elem.send_keys(Keys.RETURN)
elem = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, 'PDF'))
)
elem = driver.find_element_by_link_text('PDF')
elem.click()
