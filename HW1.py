import requests
from pprint import pprint


params = {'v': '5.131',
          'access_token': 'cce2387ccb454854b65a952e113c1a04f0e78ebfa3846cd51a924ba41c4757d461282e85b8130d96bd860',
          'user_id': '868587',
          'extended': '0'}
url = 'https://api.vk.com/method/groups.get'
response = requests.get(url, params=params)
with open ('vk_groups.json', 'w', encoding=response.encoding) as f:
    f.write(response.text)