import requests
from yarl import URL
from bs4 import BeautifulSoup
from random import choice

def grab_pics_from_yandex(request_string='фитнес бикини фото'):

    yandex_search_url = '''https://yandex.ru/images/search?text=
    %D1%84%D0%B8%D1%82%D0%BD%D0%B5%D1%81%20%D0%B1%D0%B8%D0%BA%D0%B
    8%D0%BD%D0%B8%20%D1%84%D0%BE%D1%82%D0%BE'''

    search_url = URL(yandex_search_url)

    build_url = search_url.with_query({'text': request_string})

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
    }
    page = requests.get(build_url, headers=headers)

    if page.status_code == 200:
        page = BeautifulSoup(page.text, 'html.parser') 

    imgs = page.select('.serp-item__link')
    img_links = [ img['href'] for img in imgs ] 

    pic_num = choice(list(range(len(img_links))))
    img_page_url = URL(img_links[pic_num])
    img_page_url = URL(img_page_url.query['img_url'])

    img = requests.get(img_page_url)

    filename = f'picture{pic_num}.png'
    with open(filename, 'wb') as file:
        file.write(img.content)

    return filename


