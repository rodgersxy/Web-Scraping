import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

# Get the absolute path to the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the ChromeDriver executable
chromedriver_path = os.path.join(current_dir, "chromedriver")

# Specify the path to the Chrome binary
chrome_binary_path = "/usr/bin/google-chrome"

# Create a Service object with the ChromeDriver executable path and Chrome binary path
service = Service(executable_path=chromedriver_path, chrome_binary=chrome_binary_path)

# Create a new instance of the Chrome driver with the specified Service
driver = webdriver.Chrome(service=service)

# Navigate to the Google Maps search page
url = "https://www.google.com/maps"
driver.get(url)

# Find the search box and enter the query
search_box = driver.find_element_by_id("searchboxinput")
search_box.send_keys("restaurants in Nairobi")
search_box.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(5)  # Adjust the delay as needed

# Get the page source after the dynamic content has loaded
html_content = driver.page_source

# Parse the HTML content with BeautifulSoup
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find the restaurant elements
restaurants = soup.find_all("div", class_="section-result-details-container")

# Extract the data from the restaurant elements
for restaurant in restaurants:
    name = restaurant.find("h3", class_="section-result-title").text.strip()
    address = restaurant.find("span", class_="section-result-location").text.strip()
    print("Name:", name)
    print("Address:", address)
    print("-" * 50)

# Close the browser
driver.quit()