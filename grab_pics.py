from urllib.request import ProxyBasicAuthHandler
import requests
import time
from yarl import URL
from bs4 import BeautifulSoup
from random import choice, choices, randint

def get_numbers_of_pages_to_scan(pics_quantity): 

    start_page_num = randint(0, pics_quantity * 2)
    pages_span = pics_quantity

    return choices(list(range(start_page_num, start_page_num + pages_span)), k=pics_quantity)

def grab_pics_from_yandex(quantity, request_string):

    yandex_search_url = '''https://yandex.ru/images/search?text=
    %D1%84%D0%B8%D1%82%D0%BD%D0%B5%D1%81%20%D0%B1%D0%B8%D0%BA%D0%B
    8%D0%BD%D0%B8%20%D1%84%D0%BE%D1%82%D0%BE'''

    search_url = URL(yandex_search_url)

    img_links = []
    for p in get_numbers_of_pages_to_scan(quantity):
        build_url = search_url.with_query({'p': str(p), 'text': request_string})

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'
        }
        
        try:
            page = requests.get(build_url, headers=headers)
        except Exception as msg:
            print(msg)
            continue   

        if page.status_code == 200:
            page = BeautifulSoup(page.text, 'html.parser') 

            imgs = page.select('.serp-item__link')
            img_links.extend([img['href'] for img in imgs])
            print(f'got {len(img_links)} links')
            time.sleep(5) 

    pic_num = choices(list(range(len(img_links))), k = quantity * 2)

    filenames = []
    for num in pic_num:
        img_page_url = URL(img_links[num]).query['img_url']
       
        img = requests.get(img_page_url)
        if img.status_code == 200:
            filename = f'picture{num}.png'
            with open(filename, 'wb') as file:
                file.write(img.content)
            
            filenames.append(filename)
        if len(filenames) == quantity:
            break

    return filenames

