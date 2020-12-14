'''
Заходите на ось цей сайт
https://www.expireddomains.net/register-deleted-domains/
(з ним будьте обережні) вибираєте будь-яку на ваш вибір доменну зону і
парсите список  доменів - їх там буде десятки тисяч
(звичайно ураховуючи пагінацію)
Всі отримані значення зберігти в CSV файл.
'''

import requests
from bs4 import BeautifulSoup
import os
import csv
from time import sleep


path = fr"{os.path.dirname(__file__)}"

main_url = "https://www.expireddomains.net"
# page to scrap (filter '.net')
url = "https://www.expireddomains.net/deleted-domains/?&ftlds[]=3#listing"
# delay time between scraps
delay = 10


def main(url):
    if not os.path.exists(f"{path}/domains_data.csv"):
        with open(f"{path}/domains_data.csv", "w", encoding="utf-8", newline='') as f:
            fields = ["Domain", "BL", "DP", "ABY", "ACR", "Alexa", "Dmoz",
                      "C", "N", "O", "D", "Reg", "RDT", "Dropped", "Status"]
            file_writer = csv.DictWriter(f, delimiter=",", fieldnames=fields)
            file_writer.writeheader()
    while True:
        session = requests.Session()
        session.headers = {'accept-encoding': 'gzip, deflate, br',
                           'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                           'cache-control': 'no-cache',
                           'dnt': '1',
                           'pragma': 'no-cache',
                           'sec-fetch-dest': 'document',
                           'sec-fetch-mode': 'navigate',
                           'sec-fetch-site': 'none',
                           'sec-fetch-user': '?1',
                           'upgrade-insecure-requests': '1',
                           'referer': f'{url}',
                           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
                          }
        sleep(delay)
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        get_data(soup)
        if next_page(soup):
            sleep(delay)
            continue
        else:
            break


def get_data(soup):
    ''' collect all necessary data from page '''
    all_domains = soup.select('.base1>tbody>tr')
    for domain in all_domains:
        data = []
        data.append(domain.select_one('.namelinks').text)
        data.append(domain.select_one('.bllinks').text)
        data.append(domain.select_one('.field_domainpop').text)
        data.append(domain.select_one('.field_abirth').text)
        data.append(domain.select_one('.field_aentries').text)
        data.append(domain.select_one('.field_alexa').text)
        data.append(domain.select_one('.field_dmoz').text)
        data.append(domain.select_one('.field_statuscom').text)
        data.append(domain.select_one('.field_statusnet').text)
        data.append(domain.select_one('.field_statusorg').text)
        data.append(domain.select_one('.field_statusde').text)
        data.append(domain.select_one('.field_statustld_registered').text)
        data.append(domain.select_one('.field_related_cnobi').text)
        data.append(domain.select_one('.field_changes').text)
        try:
            data.append(main_url + domain.select_one('.field_whois>a').get('href'))
        except AttributeError:
            data.append('Unavailable')
        write_data(data)
    return


def next_page(soup):
    ''' make link to next page (if available) '''
    try:
        page = soup.select_one('a[class="next"]').get('href')
        url = main_url + page
        return url
    except AttributeError:
        return False


def write_data(data):
    ''' write data to csv-file '''
    with open(f"{path}/domains_data.csv", "a+", encoding="utf-8", newline='') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(data)
    return


if __name__ == '__main__':
    main(url)
