"""Scrape all image links from the Van Gogh museum website.

Uses Playwright to launch a headless Chrome browser, navigate to the museum 
website, scroll to load more images, then parse the HTML to extract all image 
links and titles into a list of dicts.

Returns:
    List of dicts with keys "link" and "title" for each image.
"""
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import httpx
from typing import List

# Scrape all image links
async def scrape_image_links():
    # Intitialize an async playwright instance
    async with async_playwright() as playwight:
        # Launch a chrome headless browser
        browser = await playwight.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.vangoghmuseum.nl/en/collection")
        await page.mouse.wheel(0, 500)
        await page.wait_for_load_state("networkidle")
        # parse product links from HTML
        page_content = await page.content()
        image_links = []
        soup = BeautifulSoup(page_content, "html.parser")
        for image_box in soup.select("div.collection-art-object-list-item"):
            result = {
                "link": image_box.select_one("img")
                .attrs["data-srcset"]
                .split("w,")[-1]
                .split(" ")[0],
                "title": image_box.select_one("img").attrs["alt"],
            }
            image_links.append(result)
        return image_links

image_links = asyncio.run(scrape_image_links())

async def scrape_images(image_links: List):
    client = httpx.AsyncClient()
    for image_object in image_links:
        with open(f"./images/{image_object['title']}.jpg", "wb") as file:
            image = await client.get(image_object["link"])
            file.write(image.content)
            print(f"Image {image_object['title']} has been scraped")

asyncio.run(scrape_images(image_links))
