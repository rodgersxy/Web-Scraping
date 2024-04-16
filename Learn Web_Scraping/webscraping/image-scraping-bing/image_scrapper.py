import httpx
from bs4 import BeautifulSoup
import os

# 1. Find image links on the website
image_links = []
# Scrape the first 4 pages
for page in range(4):
    url = f"https://web-scraping.dev/products?page={page}"
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for image_box in soup.select("div.row.product"):
        result = {
            "link": image_box.select_one("img").attrs["src"],
            "title": image_box.select_one("h3").text,
        }
        # Append each image and title to the result array
        image_links.append(result)

# Create the 'images' directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# 2. Download image objects
for image_object in image_links:
    # Create a new .png image file
    with open(f"./images/{image_object['title']}.png", "wb") as file:
        image = httpx.get(image_object["link"])
        # Save the image binary data into the file
        file.write(image.content)
        print(f"Image {image_object['title']} has been scraped")
