"""Scrapes image links and downloads images from the Lyst homepage.

Uses httpx to fetch the homepage HTML. Parses the page with BeautifulSoup 
to extract the script tag containing JSON data. Extracts the JSON using a regex.
Loads the JSON and uses JMESPath to extract image link dictionaries. 
Downloads each image to a local file using the URL and alt text from the dicts.
"""
import httpx
from bs4 import BeautifulSoup
import json
import jmespath
import re

request = httpx.get("https://www.lyst.com/")
soup = BeautifulSoup(request.text, "html.parser")

script_tag = soup.select_one("script[data-hypernova-key=HomepageLayout]").text

# Extract JSON data from the HTML
data_match = re.search(r"<!--(.*?)-->", script_tag, re.DOTALL)
data = data_match.group(1).strip()

# Select the image data dictionary
json_data = json.loads(data)["layoutData"]["homepage_breakout_brands"]

# JMESPath search expressions
expression = {
    "designer_images": "designer_links[*].{image_url: image_url, image_alt: image_alt}",
    "top_dc_images": "top_dc_links[*].{image_url: image_url, image_alt: image_alt}",
    "bottom_dc_images": "bottom_dc_links[*].{image_url: image_url, image_alt: image_alt}",
}

# Use JMESPath to extract the values
designer_images = jmespath.search(expression["designer_images"], json_data)
top_dc_images = jmespath.search(expression["top_dc_images"], json_data)
bottom_dc_images = jmespath.search(expression["bottom_dc_images"], json_data)
image_links = designer_images + top_dc_images + bottom_dc_images

for image_object in image_links:
    with open(f"./images/{image_object['image_alt']}.jpg", "wb") as file:
        image = httpx.get(image_object["image_url"])
        file.write(image.content)
        print(f"Image {image_object['image_alt']} has been scraped")