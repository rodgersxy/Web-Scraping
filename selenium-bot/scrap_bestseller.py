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

# pagination
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')

# Get the last page number, or set a default value of 1 if it fails
try:
    last_page = int(pages[-2].text)
except ValueError:
    last_page = 1

current_page = 1

book_title = []
book_author = []
book_length = []

while current_page <= last_page:
    time.sleep(3)
    # Find the container element by its class name
    container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
    products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')
    for product in products:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)
    current_page = current_page + 1
    try:
        next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books_bestseller.csv', index=False)