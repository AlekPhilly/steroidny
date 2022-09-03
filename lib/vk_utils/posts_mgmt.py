import requests
import datetime
import time
import sys
from yarl import URL
from ..constants import ID, TOKEN, VERSION

def build_vk_api_url(method: str, method_query: dict) -> URL:
    '''
    build vk api url for steroid dudes
    method <str> - method name
    method query <dict> - method query params
    '''
    
    api_url = URL('https://api.vk.com/method/')
    
    access = {
    'access_token': TOKEN,
    'v': VERSION
    }

    query = {**method_query, **access}

    url_kwargs = {
        'scheme': api_url.scheme,
        'host': api_url.host,
        'path': api_url.path + method,
        'query': query
    }

    return URL.build(**url_kwargs)


def get_postponed_posts(count):
    
    method = 'wall.get'

    method_query = {
        'owner_id': '-' + ID,
        'count': str(count),
        'filter': 'postponed'
    }

    wall_get_url = build_vk_api_url(method, method_query)

    wall_posts = requests.get(wall_get_url)
    content = wall_posts.json()
    
    return content


def check_postponed_posts_dates(count):

    posts = get_postponed_posts(count)
    try:
        post_dates = [datetime.date.fromtimestamp(post['date'])
                        for post in posts['response']['items']]
    except IndexError:
        print('no postponed posts')
        return None
    except KeyError: 
        # got an error (response has no 'response' field)
        print(posts['error']['error_msg'])
        sys.exit(1)
    
    return post_dates


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
 
    method = 'photos.getWallUploadServer'

    method_query = {
        'group_id': ID
    }

    upload_server_url = build_vk_api_url(method, method_query)
    upload_server = requests.get(upload_server_url)

    try:
        url = upload_server.json()['response']['upload_url']
    except KeyError:
        print("Can't upload photo: ", end='')
        print(upload_server.json()['error']['error_msg'])
        sys.exit(1)

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