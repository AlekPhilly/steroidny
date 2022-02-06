import datetime
import time
import requests
from yarl import URL
from grab_pics import grab_pics_from_yandex
import sys
from pathlib import Path


ID = Path('input.txt').read_text().splitlines()[0]
TOKEN = Path('input.txt').read_text().splitlines()[1]
REQUEST = Path('input.txt').read_text().splitlines()[2]
MESSAGE = Path('input.txt').read_text().splitlines()[3]

def build_vk_api_url(method, method_query):
    '''
    build vk api url for steroid dudes
    method <str> - method name
    method query <dict> - method query params
    '''
    global TOKEN
    
    api_url = URL('https://api.vk.com/method/')
    # token with access to the wall and photos, unlimited due date
    
    access = {
    'access_token': TOKEN,
    'v': '5.120'
    }

    query = {**method_query, **access}

    url_kwargs = {
        'scheme': api_url.scheme,
        'host': api_url.host,
        'path': api_url.path + method,
        'query': query
    }

    return URL.build(**url_kwargs)

def calc_publish_date(start_datetime=None, shift_days=0):

    if not start_datetime:
        start_datetime = datetime.datetime.now()
    
    publish_date = start_datetime + datetime.timedelta(days=shift_days)
    publish_date = str(time.mktime(publish_date.timetuple()))

    return publish_date

def publish_photo(photo_path, publish_date, message='Картинка дня'):
    '''
    Schedule photo publishing to the wall of the 
    public 'Steroid Dudes' with the given message.

    photo_path <str>: path to the file (.png)
    message <str>: message text
    publish_date <str(unixtime)>: publish_date
    '''
    global ID

    method = 'photos.getWallUploadServer'

    method_query = {
        'group_id': ID
    }

    upload_server_url = build_vk_api_url(method, method_query)
    upload_server = requests.get(upload_server_url)

    url = upload_server.json()['response']['upload_url']

    photo = {
        'file': open(photo_path, 'rb')
    }

    upload_photo = requests.post(url, files=photo).json()

    method = 'photos.saveWallPhoto'
    save_photo_params = {
        'group_id': ID,
        'photo': upload_photo['photo'],
        'server': upload_photo['server'],
        'hash': upload_photo['hash']
    }

    save_photo = requests.get(build_vk_api_url(method, save_photo_params))
    owner_id = str(save_photo.json()['response'][0]['owner_id'])
    photo_id = str(save_photo.json()['response'][0]['id'])

    # create post
    method = 'wall.post'

    method_query = {
        'owner_id': '-' + ID,
        'from_group': '1',
        'message': message,
        'attachments': f'photo{owner_id}_{photo_id}'
    }

    if publish_date:
        method_query['publish_date'] = publish_date

    # publish post
    wall_post_get_url = build_vk_api_url(method, method_query)
    requests.get(wall_post_get_url)

def get_wall_posts(count):
    
    method = 'wall.get'

    method_query = {
        'owner_id': '-' + ID,
        'count': str(count)
    }

    wall_get_url = build_vk_api_url(method, method_query)

    wall_posts = requests.get(wall_get_url)
    content = wall_posts.json()
    
    return content

def remove_pics():
    files = Path().glob('*.png')
    for file in files:
        file.unlink()

    return

def main(days=5, delay=1):

    global REQUEST
    global MESSAGE
    
    request_string = REQUEST
    start_date = datetime.date.today() + datetime.timedelta(days=delay)
    start_time = datetime.time(9, 0)
    start_datetime = datetime.datetime.combine(start_date, start_time)

    photo_paths = grab_pics_from_yandex(days, request_string)
    print()
    for day, photo in enumerate(photo_paths):
        publish_date = calc_publish_date(start_datetime, day)
        try: # TODO: fix function to accept bad vk response 
            publish_photo(photo, publish_date, message=MESSAGE)
            print(f'published {photo} on {datetime.datetime.fromtimestamp(float(publish_date))}')
        except KeyError as e:
            continue
       # time.sleep(1)
    return

if __name__ == '__main__':
    if len(sys.argv) == 3:
        days = int(sys.argv[1])
        delay = int(sys.argv[2])
    elif len(sys.argv) == 2:
        days = int(sys.argv[1])
        delay = 1

    main(days, delay)
    remove_pics()

# TODO: force function to post pics from the hard drive
