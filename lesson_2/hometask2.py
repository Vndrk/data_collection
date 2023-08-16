import requests as r
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd


session = r.session()
job_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
params = {'page': 0}
vacancy = input('Введите вакансию для поиска:')
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

df_vac = pd.DataFrame(job_list)
print(df_vac)
df_vac.to_csv('job_search.csv', index=False)
