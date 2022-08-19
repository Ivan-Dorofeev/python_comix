import os
import requests
from dotenv import load_dotenv


def get_auth_token(client_id):
    url = 'https://oauth.vk.com/authorize'
    uploads = {
        'client_id': client_id,
        'display': 'mobile',
        'scope': 'photos,groups,wall,offline',
        'response_type': 'token',
    }

    response = requests.get(url, params=uploads)
    response.raise_for_status()
    return response.url


if __name__ == '__main__':
    load_dotenv()
    client_id = os.environ['APPS_CLIENT_ID']
    token_url = get_auth_token(client_id)
    print("Перейди по ссылки и скопируй token", token_url)
