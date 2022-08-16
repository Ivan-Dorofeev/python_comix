import os
from pprint import pprint

import requests
from dotenv import load_dotenv


def get_all_my_groups():
    load_dotenv()

    url = 'https://api.vk.com/method/groups.get'
    token = os.environ['ACCESS_TOKEN']
    params = {'access_token': token,
              'v': 5.131,

              'user_id': '',
              'extended': '',
              'filter': '',
              'fields': '',
              'offset': '',
              'count': '',
              }

    response = requests.get(url, params=params)
    print(response.text)
    response.raise_for_status()


def get_upload_address():
    load_dotenv()

    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    token = os.environ['ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']
    params = {
        'access_token': token,
        'v': 5.131,

        'group_id': group_id,
    }

    response = requests.get(url, params=params)
    pprint(response.json())
    response.raise_for_status()

    getted_upload_address = response.json()['response']
    return getted_upload_address


def load_photo_to_server(upload_address):
    with open(os.path.join('files', '90s_flowchart.png'), 'rb') as file:
        url = upload_address['upload_url']
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        pprint(response.json())
        response.raise_for_status()

    return response.json()


def save_photo_in_group_album(info_from_server, upload_address):
    load_dotenv()

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    token = os.environ['ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']
    params = {
        'access_token': token,
        'v': 5.131,

        'user_id': upload_address['user_id'],
        'group_id': group_id,
        'photo': info_from_server['photo'],
        'server': info_from_server['server'],
        'hash': info_from_server['hash'],
        'latitude': '',
        'longitude': '',
        'caption': 'картинка комикса',
    }

    response = requests.post(url, params=params)
    pprint(response.json())
    response.raise_for_status()


if __name__ == '__main__':
    upload_address = get_upload_address()
    info_from_server = load_photo_to_server(upload_address)
    save_photo_in_group_album(info_from_server, upload_address)
