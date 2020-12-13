'''
Написати скрипт, який буде приймати на вхід ID категорії із сайту
https://rozetka.com.ua і буде збирати всі товари із цієї категорії,
збирати по ним всі можливі дані і зберігати їх у CSV файл.
(наприклад, якщо категорія має ID 12345,
то файл буде називатись 12345_products.csv
'''


import requests
from bs4 import BeautifulSoup
import os
import csv
import re


main_url = 'https://rozetka.com.ua/'

# link for target category
category = 'mobile-phones/c80003/'
cat_id = category.split('/')[-2]

path = fr"{os.path.dirname(__file__)}"


def main():
    if not os.path.exists(f"{path}/{cat_id}_products.csv"):
        with open(f"{path}/{cat_id}_products.csv", "w", encoding="utf-8", newline="") as f:
            fields = ["PRODUCT", "PRICE", "DESCRIPTION"]
            file_writer = csv.DictWriter(f, delimiter=",", fieldnames=fields)
            file_writer.writeheader()
    i = 1
    while True:
        url = f'{main_url}{category}page={i}/'
        response = requests.get(url)
        if response.ok:
            get_links(response)
            i += 1
            continue
        else:
            print("Finished")
            break


def get_links(response):
    ''' return list of links for all products on a page '''
    soup = BeautifulSoup(response.text, 'lxml')
    bs_links = soup.select('a[class="goods-tile__picture"]')
    links = []
    for link in bs_links:
        links.append(link.get('href'))
    get_info(links)
    return


def get_info(links):
    ''' collect all necessary information about product '''
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')

        product_data = []
        # product`s title
        title = soup.select_one('h1[class="product__title"]')
        product_data.append(title.text.strip())
        # product`s price
        price_pattern = r'"price":"(.*?)"'
        price = re.findall(price_pattern, response.text)[0]
        product_data.append(price.strip())
        # product`s text description (if available)
        try:
            description = soup.select_one('p[class="product-about__brief"]')
            product_data.append(description.text.strip())
        except AttributeError:
            product_data.append("No description")

        write_file(product_data)
    return


def write_file(product_data):
    ''' write data to file '''
    with open(f"{path}/{cat_id}_products.csv", "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(product_data)
    return


if __name__ == '__main__':
    main()
