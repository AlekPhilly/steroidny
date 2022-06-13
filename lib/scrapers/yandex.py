from random import randint, sample, choice
import datetime
from io import BytesIO
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from yarl import URL
from PIL import Image


def get_numbers_of_pages_to_scan(pics_quantity): 

    MAX_PAGES = 40
    SPAN = 100

    start_page_num = randint(0, datetime.datetime.now().day * randint(1, SPAN)) % (MAX_PAGES // 2)
    pages_span = datetime.datetime.now().day
    stop_page_num = (start_page_num + pages_span if start_page_num + pages_span <= MAX_PAGES
                    else MAX_PAGES)

    return sample(list(range(start_page_num, stop_page_num)), k=pics_quantity)


def get_img_links(request_string, pages_qty):

    yandex_search_url = '''https://yandex.ru/images/search?text=
    %D1%84%D0%B8%D1%82%D0%BD%D0%B5%D1%81%20%D0%B1%D0%B8%D0%BA%D0%B
    8%D0%BD%D0%B8%20%D1%84%D0%BE%D1%82%D0%BE'''

    search_url = URL(yandex_search_url)
    img_links = set()

    for p in get_numbers_of_pages_to_scan(pages_qty):

        build_url = search_url.with_query({'p': str(p), 'text': request_string})

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0)' \
            ' Gecko/20100101 Firefox/100.0'
        }
        
        try:
            page = requests.get(build_url, headers=headers)
        except Exception as msg:
            print(msg)
            continue   

        if page.status_code == 200:
            page = BeautifulSoup(page.text, 'html.parser') 

            imgs = page.select('.serp-item__link')
            img_links.update(URL(img['href']).query['img_url'] for img in imgs)
            
            print(f'got {len(imgs)} links from page {p}')

            if pages_qty > 1:
                datetime.time.sleep(randint(1, 5)) 
    
    return img_links    


def download_imgs(links, img_folder='./images', min_dim=600):

    Path(img_folder).mkdir(exist_ok=True)

    img_num = len(list(Path(img_folder).glob('*.png')))
    img_prefix = (str(datetime.datetime.now().month) + '-' 
                + str(datetime.datetime.now().day))
    errors = 0
    bad_qual = 0
    counter = 0
    for url in iter(links):
        # print(f'{counter} links processed')
        try:
            img = BytesIO(requests.get(url).content)
            with Image.open(img) as im:
                if all(dim >= min_dim for dim in im.size):
                    filename = f'picture-{img_prefix}_{img_num}.png'
                    im.save(Path(img_folder) / filename, 'png')
                    # print(f'image {img_prefix}_{img_num} saved')
                    img_num += 1
                else: 
                    bad_qual += 1
                counter += 1

        except Exception as e:
            #print(url, e, sep='\n')
            errors += 1
            counter += 1
            continue
        
    # print(len(links) - errors - bad_qual, 'images downloaded')
    # print(errors, 'bad links')
    # print(bad_qual, 'bad quality')


