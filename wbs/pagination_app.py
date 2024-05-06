import requests
from bs4 import BeautifulSoup

root = 'https://subslikescript.com'
website = f'{root}/movies'

result = requests.get(website)
soup = BeautifulSoup(result.text, 'html.parser')


# pagination
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

for page in range(1, int(last_page) +1)[:2]:  # range(1, 1825)
    # https://subslikescript.com/movies?page=1
    website = f'{root}/movies?page={page}'
    result = requests.get(website)
    soup = BeautifulSoup(result.text, 'html.parser')



    box = soup.find('article', class_='main-article')

    links = []

    for link in box.find_all('a', href=True):
        links.append(link['href'])

    for link in links:
        website = f'{root}{"/" if not link.startswith("/") else ""}{link}'  # Adding a slash if missing
        result = requests.get(website)
        soup = BeautifulSoup(result.text, 'html.parser')
        box = soup.find('article', class_='main-article')

        title = box.find('h1').get_text()
        transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

        with open(f'{title}.txt', 'w') as file:
            file.write(transcript)
