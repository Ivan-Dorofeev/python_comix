import os
import requests
from dotenv import load_dotenv

load_dotenv()
client_id = os.environ['APPS_CLIENT_ID']

url = 'https://oauth.vk.com/authorize'
params = {'client_id': client_id,
          'redirect_uri': 'https://yandex.ru',
          'display': 'page',
          'scope': 262148,
          'response_type': 'token',
          'state': '',
          'revoke': '',
          }

response = requests.get(url, params=params)
response.raise_for_status()

print(response.text)
