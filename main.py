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


def save_photo_in_group_album(info_from_server, upload_address, token, group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
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
    response.raise_for_status()
    return response.json()['response']


def publish_photo(comment, saved_photo, token, group_id):
    url = 'https://api.vk.com/method/wall.post'

    photo_id = saved_photo[0]['id']
    photo_owner_id = saved_photo[0]['owner_id']

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


def delete_file_and_comment(file):
    os.remove(file)


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']

    file_path, comment = download_random_comic()

    upload_address = get_upload_address(token=token, group_id=group_id)
    response_from_server = load_photo_to_server(upload_address, file=file_path)
    saved_photo = save_photo_in_group_album(response_from_server, upload_address, token=token, group_id=group_id)
    publish_photo(comment=comment, saved_photo=saved_photo, token=token, group_id=group_id)

    delete_file_and_comment(file_path)
