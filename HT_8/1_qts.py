"""
http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної
інформації про записи: цитата, автор, інфа про автора...

Збирається інформація (цитата, автор, місце і дата народження автора)
з 10 сторінок сайту
"""


import requests
from bs4 import BeautifulSoup


url = 'https://quotes.toscrape.com/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')

paginator = soup.select_one('li[class="next"]')
page = paginator.select_one('a').get('href')

i = 1
for i in range(1, 11):
    next_page = url + page[1:-2] + str(i) + '/'
    page_response = requests.get(next_page)

    soup = BeautifulSoup(page_response.text, 'lxml')
    quotes = soup.select('div[class="quote"]')

    for quote in quotes:
        soup_text = quote.select_one('span[class="text"]')
        text = (soup_text if soup_text else ''
                ).text.strip().replace('“', '').replace('”', '')

        soup_author = quote.select_one('small[class="author"]')
        author = (soup_author if soup_author else '').text.strip()

        link = quote.select_one('a').get('href')
        author_url = url + link[1:]

        author_resp = requests.get(author_url)
        auth_soup = BeautifulSoup(author_resp.text, 'lxml')
        date = auth_soup.select_one(
            'span[class="author-born-date"]').text
        orig = auth_soup.select_one(
            'span[class="author-born-location"]').text

        print(f'{text}\n{author}\nBorn: {date} {orig}\n')

    i += 1


if __name__ == '__main__':
    pass
