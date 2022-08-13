import os

import requests
from dotenv import load_dotenv


def main():
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


if __name__ == '__main__':
    main()
