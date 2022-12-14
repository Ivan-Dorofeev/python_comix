import os.path
import random

import requests
from urllib.parse import urlparse


def download_random_comic():
    max_pages = 2660

    random_number_page = random.randint(1, max_pages)
    img_url = f"https://xkcd.com/{random_number_page}/info.0.json"
    response = requests.get(img_url)
    response.raise_for_status()
    img_page = response.json()

    url_img = img_page['img']
    comment = img_page['alt']
    *_, img_filename = urlparse(url_img).path.split('/')

    response_img = requests.get(url_img)
    response_img.raise_for_status()

    if not os.path.exists('files'):
        os.makedirs('files')

    file_path = os.path.join('files', img_filename)

    with open(file_path, 'wb') as img_file:
        img_file.write(response_img.content)

    return file_path, comment


if __name__ == '__main__':
    download_random_comic()
