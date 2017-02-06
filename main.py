import requests, time
from bs4 import BeautifulSoup


def spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'https://www.avito.ru/moskva/noutbuki?p=' + str(page)
        src_code = requests.get(url)
        plain_text = src_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for link in soup.findAll('a', {'class': 'item-description-title-link'}):
            href = 'https://www.avito.ru' + link.get('href')
            title = link.string
            print(title, href)
            get_price(href)
            time.sleep(3)
        page += 1
        break


def get_price(url):
    src_code = requests.get(url)
    plain_text = src_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.findAll('span', {'class': 'price-value-string'}):
        price = link.get_text()
        print(price)
        break


spider(1)
