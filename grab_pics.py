import requests
import time
from yarl import URL
from bs4 import BeautifulSoup
from random import choice, choices, randint

def get_numbers_of_pages_to_scan(pics_quantity, selection_pct):
    
    num = round(pics_quantity/selection_pct/30)
    start_page = randint(0, 20)
    stop_page = start_page + num
    
    return range(start_page, stop_page + 1)


def grab_pics_from_yandex(quantity, request_string='фитнес бикини фото'):

    yandex_search_url = '''https://yandex.ru/images/search?text=
    %D1%84%D0%B8%D1%82%D0%BD%D0%B5%D1%81%20%D0%B1%D0%B8%D0%BA%D0%B
    8%D0%BD%D0%B8%20%D1%84%D0%BE%D1%82%D0%BE'''

    search_url = URL(yandex_search_url)

    img_links = []
    for p in get_numbers_of_pages_to_scan(quantity, 0.15):
        build_url = search_url.with_query({'p': str(p), 'text': request_string})

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
        }
        
        try:
            page = requests.get(build_url, headers=headers)
        except Exception as msg:
            print(msg)
            continue   

        if page.status_code == 200:
            page = BeautifulSoup(page.text, 'html.parser') 

        imgs = page.select('.serp-item__link')
        img_links.extend([ img['href'] for img in imgs ])
        time.sleep(30) 

    pic_num = choices(list(range(len(img_links))), k=quantity)

    filenames = []   
    for num in pic_num:
        img_page_url = URL(img_links[num])
        img_page_url = URL(img_page_url.query['img_url'])

        try:
            img = requests.get(img_page_url)
        except Exception as msg:
            print(msg)
            continue
        
        filename = f'picture{num}.png'
        with open(filename, 'wb') as file:
            file.write(img.content)
        
        filenames.append(filename)

    return filenames

