from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

web = "https://www.audible.com/adblbestsellers?ref_pageloadid=mXkHD7JLzWGjRtGA&ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=334a4a9c-12d2-4c3f-aee6-ae0cbc6a1eb0&pf_rd_r=15P9X5A66NAPD69CHFD3&pageLoadId=H2aVEGvEjCLR5ZOc&creativeId=7ba42fdf-1145-4990-b754-d2de428ba482"
path = "/home/rodgers/Downloads/chrome-linux64/chrome"

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = path
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
driver.get(web)

book_title = []
book_author = []
book_length = []

# Function to scrape data from the current page
def scrape_page():
    container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
    products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')
    for product in products:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

# Scrape the initial page
scrape_page()

# Scroll to the bottom of the page to load more content
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for the page to load more content
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    scrape_page()

driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books_bestsellerv2.csv', index=False)