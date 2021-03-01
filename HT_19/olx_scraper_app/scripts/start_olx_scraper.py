# celery -A HT_19 worker -Q olx_scraper_app

import re
import requests
from bs4 import BeautifulSoup

from HT_19.celery import app
from olx_scraper_app.models import ScrapedOlxAd

main_url = 'https://www.olx.ua'


@app.task(name='olx_scraper_app.scripts.start_olx_scraper.limiter_of_ads_number', queue='olx_scraper_app')
def limiter_of_ads_number(target_ads, category):
    page = 1
    while target_ads > 0:
        url = f'{main_url}/{category}/?page={page}'
        target_ads -= get_ads_pages_links(url, target_ads)
        page += 1


def get_ads_pages_links(url, target_ads):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.select('h3[class="lheight22 margintop5"]')
        ad = 0
        for link in links:
            if ad < target_ads:
                if get_ad_and_author_info(link.select_one('a').get('href')):
                    ad += 1
        return ad
    else:
        exit()


def get_ad_and_author_info(ad_link):
    referer_link = get_referer_link(ad_link)
    session = requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                       'Referer': referer_link
                       }
    response = session.get(ad_link)
    soup = BeautifulSoup(response.text, 'lxml')

    try:
        # get ad title
        ad_title = soup.select_one('div[class="layertitle__title"]').text.strip()

        # get ad text
        ad_text = soup.select_one('div[id="textContent"]').text.strip()

        # get author name
        author_name = soup.select_one('div[class="offer-user__actions"] a').text.strip()

        # get author info
        author_adress = soup.select_one('div[class="offer-user__address"]').text.strip()
        register_date = soup.select_one('div[class="userbox__user-since"]').text.strip()
        author_info = f'Местоположение: {author_adress}, зарегистрирован {register_date}'

        # get author phone number
        token_pattern = r"var phoneToken = '(.*?)';"
        id_pattern = r"'id':'(.*?)'"
        token = re.findall(token_pattern, response.text)[0]
        id_num = re.findall(id_pattern, response.text)[0]
        phone_url = f'https://www.olx.ua/ajax/misc/contact/phone/{id_num}/?pt={token}'
        get_phone = session.get(phone_url)
        raw_phone = get_phone.json()['value']
        phone = raw_phone.strip().replace('<span class="block">', '').replace('</span>', '')

        saved_data = ScrapedOlxAd.objects.filter(url=ad_link)
        if not saved_data:
            scraped_data = ScrapedOlxAd(url=ad_link,
                                        title=ad_title,
                                        text=ad_text,
                                        author_name=author_name,
                                        author_phone_number=phone,
                                        author_info=author_info)
            scraped_data.save()
            return True
        else:
            return False
    except Exception:
        return False


def get_referer_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    referer_link = soup.select_one('link[rel="alternate"]').get('href')
    return referer_link
