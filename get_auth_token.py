import os
import requests
from dotenv import load_dotenv


def get_auth_token(client_id):
    url = 'https://oauth.vk.com/authorize'
    params = {'client_id': client_id,
              'redirect_uri': '',
              'display': 'mobile',
              'scope': 'photos,groups,wall,offline',
              'response_type': 'token',
              'state': '',
              'revoke': '',
              }

    response = requests.get(url, params=params)
    response.raise_for_status()
    print("Перейди по ссылки и скопируй token", response.url)


if __name__ == '__main__':
    load_dotenv()
    client_id = os.environ['APPS_CLIENT_ID']
    get_auth_token(client_id)
