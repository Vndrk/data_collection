import requests as r
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib

client = MongoClient('127.0.0.1', 27017)
db = client['jobs']
found_jobs = db.found_jobs


target_salary = int(input('Введите минимальный уровень зп:'))

session = r.session()
job_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
params = {'page': 0}
vacancy = input('Введите вакансию для поиска на hh и добавления в базу вакансий:')
url = f'https://hh.ru/search/vacancy?text={vacancy}'
while True:
    response = session.get(url, headers=headers, params=params)
    if response.status_code != 200:
        break
    soup = BeautifulSoup(response.text, 'html.parser')
    vacancies = soup.findAll('div', {'class': 'serp-item'})
    if not vacancies:
        break
    for job in vacancies:
        job_dict = {'min_salary': None,
                    'max_salary': None}
        title = job.find('a', {'class': 'serp-item__title'})
        title_name = title.text
        ref = title.get('href')
        job_dict['ref'] = ref
        job_dict['name'] = title_name
        str_hash = str(ref + title.text)
        str_hash = bytes(str_hash, encoding ='utf-8')
        job_dict['_id'] = hashlib.sha256(str_hash).hexdigest()

        try:
            salary = job.find('span', {'class': 'bloko-header-section-2'}).text.split()
            for i in range(len(salary)):
                if salary[0] == 'от':
                    salary[1] = int(salary[1] + salary[2])
                    job_dict['min_salary'] = salary[1]
                elif salary[0] == 'до':
                    salary[1] = int(salary[1] + salary[2])
                    job_dict['max_salary'] = salary[1]
                else:
                    job_dict['min_salary'] = int(salary[0] + salary[1])
                    job_dict['max_salary'] = int(salary[-3] + salary[-2])
                job_dict['currency'] = salary[-1]





        except:
            salary = None

        job_list.append(job_dict)

        params['page'] += 1

pprint(job_list)


for job in job_list:
    try:
        found_jobs.insert_one(job)
    except DuplicateKeyError:
        print(f'item  already exists')

for i in found_jobs.find({}):
    pprint(i)


# Функция возвращающая вакансии с зп выше минимального порога.
def find_job(target_salary):
    print(f'Вакансии с требуемым уровнем зп от {target_salary} RUB:')
    for job in found_jobs.find(
            {'$or': [{'min_salary': {'$gt': target_salary}}, {'max_salary': {'$gt': target_salary}}]}):
        pprint(job)



find_job(target_salary)

# found_jobs.delete_many({})
