# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
# Немного изменил вариант этого задания, и сделал ввод имя пользователя через инпут, так мне
# показалась будет интересней.

import requests
import json

user = input('Введите имя пользователя:')

url = 'https://api.github.com'  # Ссылка на github api

r = requests.get(f'{url}/users/{user}/repos')  # get запрос
j_data = r.json()


try:
    with open(f'{user}_repos.json', 'w') as f:
        json.dump(j_data, f)

    for i in j_data:
        print(i['name'])
except(NameError):
    print(f'Невозможно получить данные. Пользователя не существует')

# в качестве конкретного пользователя ввели Vndrk. Список репоситорией сохранён в json-файле Vndrk_repos.