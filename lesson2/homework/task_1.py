import json
import re

from bs4 import BeautifulSoup
import requests

url = 'https://hh.ru/search/vacancy'

# job = input('Enter the job position: ')
job = 'HR'
job_list = []
# page = int(input('Enter the number of pages: '))
pages = 2

headers = \
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/96.0.4664.110 Safari/537.36'}

for i in range(1, pages + 1):
    params = {'clusters': 'true',
              'area': 1,
              'ored_clusters': 'true',
              'enable_snippets': 'true',
              'salary': None,
              'text': job,
              'page': i,
              'hhtmFrom': 'vacancy_search_list'}

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('div', {'class': 'vacancy-serp-item'})
    for job in jobs:
        job_data = {}
        info = job.find('a')
        name = info.text
        link = info.get('href')
        salary = job.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salary is not None:
            new_salary = str(salary.text)
            if 'от' in new_salary:
                min_salary = int(re.sub("[^a-z0-9а-яА-Я]+", "", new_salary.split(' ')[1], flags=re.IGNORECASE))
                max_salary = None
                currency = new_salary.split(' ')[2]
            else:
                min_salary = int(re.sub("[^a-z0-9а-яА-Я]+", "", new_salary.split(' ')[0], flags=re.IGNORECASE))
                max_salary = int(re.sub("[^a-z0-9а-яА-Я]+", "", new_salary.split(' ')[2], flags=re.IGNORECASE))
                currency = new_salary.split(' ')[3]
        else:
            min_salary = None
            max_salary = None
            currency = None
        company = job.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
        new_company = re.sub("[^a-z0-9а-яА-Я]+", " ", company, flags=re.IGNORECASE)
        location = job.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text

        job_data['name'] = name
        job_data['link'] = link
        job_data['company'] = new_company
        job_data['location'] = location
        job_data['min_salary'] = min_salary
        job_data['max_salary'] = max_salary
        job_data['currency'] = currency

        job_list.append(job_data)

with open('jobs.json', 'w', encoding='utf-8') as f:
    json.dump(job_list, f, ensure_ascii=False)
