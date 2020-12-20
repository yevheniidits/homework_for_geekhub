import scrapy
from bs4 import BeautifulSoup
import re
import os
import csv
import requests


class RozetkaSpider(scrapy.Spider):
    name = "rozetka"
    path = fr"{os.path.dirname(__file__)}"
    if not os.path.exists(f"{path}/rozetka_products.csv"):
        with open(f"{path}/rozetka_products.csv", "w", encoding="utf-8", newline="") as f:
            fields = ["PRODUCT", "PRICE", "DESCRIPTION"]
            file_writer = csv.DictWriter(f, delimiter=",", fieldnames=fields)
            file_writer.writeheader()

    def start_requests(self):
        main_url = 'https://rozetka.com.ua/'
        # link for target category
        category = 'mobile-phones/c80003/'
        url = f'{main_url}{category}/'
        i = 1
        while True:
            url = f'{main_url}{category}page={i}/'
            response = requests.get(url)
            if response.ok:
                i += 1
                yield scrapy.Request(url, self.get_links)
            else:
                break

    def get_links(self, response):
        ''' return list of links for all products on a page '''
        soup = BeautifulSoup(response.text, 'lxml')
        bs_links = soup.select('a[class="goods-tile__picture"]')
        for link in bs_links:
            prod_link = link.get('href')
            yield scrapy.Request(prod_link, self.get_info)

    def get_info(self, response):
        ''' collect all necessary information about product '''
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
        
        # write data to file
        path = fr"{os.path.dirname(__file__)}"
        with open(f"{path}/rozetka_products.csv", "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(product_data)
