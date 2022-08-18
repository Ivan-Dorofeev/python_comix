import os.path
import random

import requests
from urllib.parse import urlparse


def download_random_comic():
    max_pages = 2660

    random_number_page = random.randint(1, max_pages)
    all_img_url = f"https://xkcd.com/{random_number_page}/info.0.json"
    response = requests.get(all_img_url)
    response.raise_for_status()
    page = response.json()

    url_img = page['img']
    comment = page['alt']
    *_, img_file = urlparse(url_img).path.split('/')
    img_name, *_ = img_file.split('.')

    response_img = requests.get(url_img)
    response_img.raise_for_status()

    file_path = os.path.join('files', img_file)

    with open(file_path, 'wb') as img_file:
        img_file.write(response_img.content)

    # with open(os.path.join('alt', f'{img_name}.txt'), 'w') as text_file:
    #     text_file.write(comment)

    return file_path, comment


if __name__ == '__main__':
    download_random_comic()
