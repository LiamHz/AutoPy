from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Enable waiting
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Read user credentials from external file
f = open("AuthenticationCredentials.txt","r")
lines = f.read().splitlines()
USERNAME = lines[13]
PASSWORD = lines[14]
f.close()

desiredSheets=[]
stillSearching = True

print("What pieces do you want to download?")
print("Type STOP when you have entered all the pieces you want.")

# Add all desired sheets to array until command 'stop' is given
while stillSearching:
    userInput = input()
    if userInput.lower() == "stop":
        stillSearching = False
    else:
        desiredSheets.append(userInput)

searchSite = "musescore.com"
sheetsIndex = 0

driver = webdriver.Chrome()

while sheetsIndex < len(desiredSheets):
    driver.get(("https://www.google.ca/search?&q=site%3A{}+{}").format(searchSite, desiredSheets[sheetsIndex]))

    # Wait until google results load
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '(//h3)[1]/a'))
    )

    # Iterate through results until a musescore link is found (prevents going to google image and video results)
    redirect = 'user/login?destination=/'
    isMusescoreLink = False
    i = 1
    while not isMusescoreLink:
        elem = driver.find_element_by_xpath(("(//h3)[{}]/a").format(i))
        link = elem.get_attribute('href')
        if 'https://musescore.com' in link:
            isMusescoreLink = True
        i += 1

    # Go to the login redirect for that Musescore result only if this is the first search
    if sheetsIndex == 0:
        link = link[:22] + redirect + link[22:]
        driver.get(("{}".format(link)))

        # Signin to Musescore
        elem = driver.find_element_by_id('edit-name')
        elem.send_keys(USERNAME)
        elem = driver.find_element_by_id('edit-pass')
        elem.send_keys(PASSWORD)
        elem.send_keys(Keys.TAB)
        elem.send_keys(Keys.TAB)
        elem.send_keys(Keys.RETURN)
    else:
        driver.get(link)

    # Download as pdf
    elem = driver.find_element_by_class_name('js-score-download-status')
    elem.send_keys(Keys.RETURN)
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'PDF'))
    )
    elem = driver.find_element_by_link_text('PDF')
    elem.click()

    sheetsIndex += 1

print("All sheets downloaded!")
