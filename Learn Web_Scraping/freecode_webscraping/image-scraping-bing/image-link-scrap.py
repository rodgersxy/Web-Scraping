import httpx
from bs4 import BeautifulSoup

request = httpx.get('https://www.lyst.com/')
soup = BeautifulSoup(request.text, "html.parser")

for i in soup.select("a.ysyxK"):
    print(i.select_one('img').attrs["src"])