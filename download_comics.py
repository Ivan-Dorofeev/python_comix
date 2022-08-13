import os.path

import requests
from urllib.parse import urlparse


def main():
    for number_file in range(405, 2658):
        all_img_url = f"https://xkcd.com/{number_file}/info.0.json"
        response = requests.get(all_img_url)
        response.raise_for_status()
        page = response.json()
        url_img = page['img']
        comment = page['alt']
        *_, img_file = urlparse(url_img).path.split('/')
        img_name, img_extension = img_file.split('.')

        response_img = requests.get(url_img)
        response_img.raise_for_status()

        with open(os.path.join('files', img_file), 'wb') as img_file:
            img_file.write(response_img.content)

        with open(os.path.join('alt', f'{img_name}.txt'), 'w') as text_file:
            text_file.write(comment)
        print('ready = ', all_img_url)


if __name__ == '__main__':
    main()
    print('ready')
