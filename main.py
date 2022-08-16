import os
import random
from pprint import pprint

import requests
from dotenv import load_dotenv


# def get_all_my_groups():
#     load_dotenv()
#
#     url = 'https://api.vk.com/method/groups.get'
#     token = os.environ['ACCESS_TOKEN']
#     params = {'access_token': token,
#               'v': 5.131,
#
#               'user_id': '',
#               'extended': '',
#               'filter': '',
#               'fields': '',
#               'offset': '',
#               'count': '',
#               }
#
#     response = requests.get(url, params=params)
#     print(response.text)
#     response.raise_for_status()


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


def load_photo_to_server(upload_address, file):
    with open(os.path.join('files', file), 'rb') as file:
        url = upload_address['upload_url']
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        pprint(response.json())
        response.raise_for_status()

    return response.json()


def find_file_comment(file):
    searched_file = file.split('.')[0] + '.txt'
    for path, dirs, files in os.walk('alt'):
        if searched_file in files:
            with open(os.path.join('alt', searched_file), 'r') as ff:
                return ff.read()
        return ''


def save_photo_in_group_album(info_from_server, upload_address, file):
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
        'caption': '',
    }

    response = requests.post(url, params=params)
    pprint(response.json())
    response.raise_for_status()
    return response.json()['response']


def publication_photo(file, saved_photo):
    load_dotenv()

    url = 'https://api.vk.com/method/wall.post'
    token = os.environ['ACCESS_TOKEN']
    negative_group_id = '-' + os.environ['GROUP_ID']

    message = find_file_comment(file)
    photo_id = saved_photo[0]['id']
    photo_owner_id = saved_photo[0]['owner_id']

    params = {
        'access_token': token,
        'v': 5.131,

        'owner_id': negative_group_id,
        'friends_only': 0,
        'from_group': 1,
        'message': message,
        'attachments': f'photo{photo_owner_id}_{photo_id}',
        'services': '',
        'signed': 1,
        'publish_date': '',
        'lat': '',
        'long': '',
        'place_id': '',
        'post_id': '',
        'guid': '',
        'mark_as_ads': 0,
        'close_comments': 0,
        'donut_paid_duration': '',
        'mute_notifications': 0,
        'topic_id': '',
        'copyright': '',
    }

    print(params['attachments'])
    response = requests.post(url, params=params)
    pprint(response.json())
    response.raise_for_status()


if __name__ == '__main__':
    for path, dirs, files in os.walk('files'):
        pictures = files
    file = random.choice(pictures)
    upload_address = get_upload_address()
    info_from_server = load_photo_to_server(upload_address, file=file)
    saved_photo = save_photo_in_group_album(info_from_server, upload_address, file=file)
    publication_photo(file=file, saved_photo=saved_photo)
