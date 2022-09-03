import datetime
from random import sample, choice
from pathlib import Path
from lib import MESSAGE, REQUEST_PARAMS
from lib import get_img_links, download_imgs
from lib import check_postponed_posts_dates, calc_publish_date, publish_photo

def grab_pics_from_yandex(pages_qty, img_folder='./images',
                    min_dim=500):

    # search links
    # TODO: cache parsed links
    for _ in range(pages_qty):
        request = choice(REQUEST_PARAMS)
        request_string = gen_request(*request)
        print(request_string)
        links = get_img_links(request_string, 1)

        # download images
        download_imgs(links, img_folder, min_dim)


def gen_request(main_word, kind, keywords, kw_sample_len=3):
    return (main_word + ' ' + choice(kind) + ' '
            + ' '.join(sample(keywords, kw_sample_len)))


def get_images(quantity, img_folder):

    PAGES_FOR_IMG_SEARCH_QTY = 3

    Path(img_folder).mkdir(exist_ok=True)

    imgs = list(Path(img_folder).glob('*.png'))

    if not imgs or len(imgs) < quantity * 2:
        grab_pics_from_yandex(PAGES_FOR_IMG_SEARCH_QTY, img_folder)
        imgs = list(Path(img_folder).glob('*.png'))

    return sample(imgs, quantity)


def refresh_postponed_posts(days_to_cover=7, img_folder='./images'):

    start_date = datetime.date.today() + datetime.timedelta(days=1)
    start_time = datetime.time(9, 0)
    start_datetime = datetime.datetime.combine(start_date, start_time)

    imgs = get_images(days_to_cover, img_folder)

    post_dates = check_postponed_posts_dates(days_to_cover)

    for day in range(days_to_cover):
        publish_date = start_datetime + datetime.timedelta(days=day)
        if publish_date.date() not in post_dates:
            publish_date = calc_publish_date(start_datetime, day)
            photo = imgs.pop()
            try:
                publish_photo(photo, publish_date, message=MESSAGE)
                print(f'published {photo} on {datetime.datetime.fromtimestamp(float(publish_date))}')
                photo.unlink()
            except Exception as e:
                print('Got an exception:', e)
                raise
                # continue


def main():
    refresh_postponed_posts()


if __name__ == '__main__':
    main()