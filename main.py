import os
import requests
from dotenv import load_dotenv

from download_comics import download_random_comic


def get_upload_address(token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': 5.131,

        'group_id': group_id,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    upload_address = response.json()['response']
    return upload_address['user_id'], upload_address['upload_url']


def load_photo_to_server(upload_url, file_path):
    with open(file_path, 'rb') as ff:
        files = {
            'photo': ff,
        }
    response = requests.post(upload_url, files=files)
    response.raise_for_status()
    server_response = response.json()

    return server_response['photo'], server_response['server'], server_response['hash']


def save_photo_in_group_album(user_id, photo, server, hash, token, group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    params = {
        'access_token': token,
        'v': 5.131,

        'user_id': user_id,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': hash,
    }

    response = requests.post(url, params=params)
    response.raise_for_status()
    server_response = response.json()['response'][0]
    return server_response['id'], server_response['owner_id']


def publish_photo(comment, token, photo_id, photo_owner_id, group_id):
    url = 'https://api.vk.com/method/wall.post'

    params = {
        'access_token': token,
        'v': 5.131,

        'owner_id': f'-{group_id}',
        'friends_only': 0,
        'from_group': 1,
        'message': comment,
        'attachments': f'photo{photo_owner_id}_{photo_id}',
        'signed': 1,
        'mark_as_ads': 0,
        'close_comments': 0,
        'mute_notifications': 0,
    }

    response = requests.post(url, params=params)
    response.raise_for_status()


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']

    file_path, comment = download_random_comic()
    try:
        user_id, upload_url = get_upload_address(vk_token, vk_group_id)
        photo, server, hash = load_photo_to_server(upload_url, file_path)
        photo_id, photo_owner_id = save_photo_in_group_album(user_id, photo, server, hash, vk_token, vk_group_id)
        publish_photo(comment, vk_token, photo_id, photo_owner_id, vk_group_id)
    finally:
        os.remove(file_path)
