from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd

website = 'https://www.adamchoi.co.uk/overs/detailed'
path = '/home/rodgers/Downloads/chrome-linux64/chrome'

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = path
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

# Use the text content and contains function to locate the "All matches" button
all_matches_button = driver.find_element(By.XPATH, '//label[contains(text(), "All matches")]')
all_matches_button.click()






matches = driver.find_elements(By.TAG_NAME, 'tr')
date = []
home_team = []
score = []
away_team = []

for match in matches:
    date.append(match.find_element(By.XPATH, './td[1]').text)
    home = match.find_element(By.XPATH, './td[2]').text
    home_team.append(home)
    print(home)
    score.append(match.find_element(By.XPATH, './td[3]').text)
    away_team.append(match.find_element(By.XPATH, './td[4]').text)

driver.quit()

df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('football_data.csv', index=False)
print(df)