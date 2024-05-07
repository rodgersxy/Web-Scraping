from selenium import webdriver

website = 'https://www.adamchoi.co.uk/overs/detailed'
path = '/home/rodgers/Downloads/chrome-linux64/chrome'
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = path

driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

all_matches_button = driver.find_element_by_xpath('//label[@analytics-event="All matches"]')

all_matches_button.click()

# driver.quit()
