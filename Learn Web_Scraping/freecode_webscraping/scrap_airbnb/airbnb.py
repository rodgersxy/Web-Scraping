from bs4 import BeautifulSoup
import requests
import pandas as pd

Names = []
prices = []
descriptions = []
reviews = []

url = "https://www.airbnb.com/s/India/homes?adults=2"
response = requests.get(url)
# print(response)
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)
next_page = soup.find("a", class_="l1ovpqvx c1ytbx3a dir dir-ltr").get("href")
# print(next_page)

complete_next_page = "https://www.airbnb.com" + next_page
# print(complete_next_page)
url = complete_next_page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# names = soup.find_all("div", class_="c14whb16 dir dir-ltr")
# print(names)

name = soup.find_all("div", class_="t1jojoys dir dir-ltr")
# print(name)

for i in name:
    n = i.text
    Names.append(n)



price = soup.find_all("span", class_="_tyxjp1")
# print(price)

for i in price:
    n = i.text
    prices.append(n)


description_list = soup.find_all("div", class_="fb4nyux s1cjsi4j dir dir-ltr")
# ...
for i in description_list:
    descriptions.append(i)



Reviews = soup.find_all("span", class_="r1dxllyb dir dir-ltr")
# print(Reviews)

for i in Reviews:
    n = i.text
    Reviews.append(n)
 
dataFrame = pd.DataFrame({
    "Names": Names,
    "prices": prices,
    "Descriptions": descriptions,
    "Reviews": Reviews
})

print(dataFrame)