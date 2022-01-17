from pprint import pprint

from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['hh_jobs']

vacancies = db.vacancies

salary = int(input('Enter your desired income per month in rub: '))

for doc in vacancies.find({'$or': [{'min_salary': {'$lte': salary}, 'max_salary': {'$gte': salary}}]}):
    pprint(doc)
