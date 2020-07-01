import datetime
import time
import requests
from yarl import URL
from grab_pics import grab_pics_from_yandex


def build_vk_api_url(method, method_query):
    '''
    build vk api url for steroid dudes
    method <str> - method name
    method query <dict> - method query params
    '''
    api_url = URL('https://api.vk.com/method/')
    # token with access to the wall and photos, unlimited due date
    token = 'c59ffe28c1e55f0aae5fa0e00fde42071b40384bf2fabccafa85f7deaf0908ec6ec970c04ccf633a48ecf'

    access = {
    'access_token': token,
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
    # upload photo
    # app_id = 7526955
    # get upload server's address

    method = 'photos.getWallUploadServer'

    method_query = {
        'group_id': '2798'
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
        'group_id': '2798',
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
        'owner_id': '-2798',
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
        'owner_id': '-2798',
        'count': str(count)
    }

    wall_get_url = build_vk_api_url(method, method_query)

    wall_posts = requests.get(wall_get_url)
    content = wall_posts.json()
    
    return content

def main():
    request_string = 'бодибилдинг звезда чемпион'
    start_datetime = datetime.datetime(2020, 7, 31, 20, 0, 0)
    days = 3

    photo_paths = grab_pics_from_yandex(days, request_string)
    for day, photo in enumerate(photo_paths):
        publish_date = calc_publish_date(start_datetime, day)
        publish_photo(photo, publish_date, message='Мужик дня')

if __name__ == '__main__':
    main()

