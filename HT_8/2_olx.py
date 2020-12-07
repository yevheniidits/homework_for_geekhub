'''
https://www.olx.ua - написати скрейпер, який буде брати
із https://www.olx.ua/sitemap.xml першу лінку, відкривати категорію
і збирати ім'я і номер з кожної об'яви.

Дані виводяться на екран та зберігаються у файл OLX_users.csv
'''


import os
import csv
import requests
from bs4 import BeautifulSoup
import time
import re

# OLX page to scrap
url = 'https://www.olx.ua/vin/'
# delay time between scraps
delay = 3

path = fr"{os.path.dirname(__file__)}"


def get_info(link):
    '''collect user`s name and phone'''
    for i in link:
        link_ref = get_ref_link(i)
        # start session
        session = requests.Session()
        session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                           'Referer': link_ref
                           }
        page_response = session.get(i)
        soup = BeautifulSoup(page_response.text, 'lxml')
        # collect user`s name
        name = ''
        bs_name = soup.select_one('div[class="offer-user__actions"] a')
        if bs_name:
            name = bs_name.text.strip()
            token_pattern = r"var phoneToken = '(.*?)';"
            id_pattern = r"'id':'(.*?)'"
            try:
                # collect user`s phone number
                token = re.findall(token_pattern, page_response.text)[0]
                id_num = re.findall(id_pattern, page_response.text)[0]
                phone_url = f'https://www.olx.ua/ajax/misc/contact/phone/{id_num}/?pt={token}'
                get_phone = session.get(phone_url)
                raw_phone = get_phone.json()['value']
                phone = raw_phone.strip().replace('<span class="block">', '').replace('</span>', '')
            except Exception:
                time.sleep(delay)
                continue
        else:
            time.sleep(delay)
            continue
        # write data to file
        with open(f"{path}/OLX_users.csv", mode="a", encoding="utf-8", newline="") as f:
            file_writer = csv.writer(f, delimiter=",")
            file_writer.writerow([name, phone])
        print(f'NAME: {name}\nPHONE: {phone}\n')
        time.sleep(delay)


def get_announcement_links(url):
    '''return list of announcement links on page'''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.select('h3[class="lheight22 margintop5"]')
    link = []
    for head in links:
        link.append(head.select_one('a').get('href'))
    return link


def next_page(url):
    '''return link to next page'''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.select_one('span[class="fbold next abs large"]')
    page = pages.select_one('a')
    # check if next page exists, else stop
    if page:
        return page.get('href')
    else:
        return False


def get_ref_link(link):
    '''return "Referer" link for announcement'''
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    link_ref = soup.select_one('link[rel="alternate"]').get('href')
    return link_ref


def main(url):
    if not os.path.exists(f"{path}/OLX_users.csv"):
        with open(f"{path}/OLX_users.csv", "w", encoding="utf-8", newline="") as f:
            fields = ["NAME", "PHONE"]
            file_writer = csv.DictWriter(f, delimiter=",", fieldnames=fields)
            file_writer.writeheader()
    while url is not False:
        get_info(get_announcement_links(url))
        url = next_page(url)
    else:
        print("FINISH")


if __name__ == '__main__':
    main(url)
