# Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json
import pprint

user_id=16150907
access_token = ' '
url = 'https://api.vk.com'
method = 'groups.get'
response = requests.get(f'{url}/method/{method}?extended=1&v=5.124&access_token={access_token}')
j_data = response.json()



with open('groups.json', 'w') as f:
    json.dump(response.json(), f)




print(response.json())