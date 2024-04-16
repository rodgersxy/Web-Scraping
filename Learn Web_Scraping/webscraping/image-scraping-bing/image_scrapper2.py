import httpx
from bs4 import BeautifulSoup

# any URL to behance gallery page
url = "https://www.behance.net/gallery/148609445/Vector-Illustrations-Negative-Space"

request = httpx.get(url)

index = 0
image_links = []

soup = BeautifulSoup(request.text, "html.parser")
for image_box in soup.select("div.ImageElement-root-kir"):
    index += 1
    result = {
                "link": image_box.select_one("img").attrs["src"],
                "title": str(index) + ".png"
            }
    image_links.append(result)
    # Scrape the first 4 images only
    if index == 4:
        break

for image_object in image_links:
    with open(f"./images/{image_object['title']}", "wb") as file:
        image = httpx.get(image_object["link"])
        file.write(image.content)
        print(f"Image {image_object['title']} has been scraped")