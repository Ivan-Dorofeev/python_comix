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
    return upload_address


def load_photo_to_server(upload_address, file):
    with open(file, 'rb') as ff:
        url = upload_address['upload_url']
        files = {
            'photo': ff,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()

    return response.json()


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
    return response.json()['response']


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
        upload_address = get_upload_address(vk_token, vk_group_id)
        response_from_server = load_photo_to_server(upload_address, file_path)

        user_id = upload_address['user_id']
        photo = response_from_server['photo']
        server = response_from_server['server']
        hash = response_from_server['hash']
        saved_photo = save_photo_in_group_album(user_id, photo, server, hash, vk_token, vk_group_id)

        photo_id = saved_photo[0]['id']
        photo_owner_id = saved_photo[0]['owner_id']
        publish_photo(comment, vk_token, photo_id, photo_owner_id, vk_group_id)
    finally:
        os.remove(file_path)
