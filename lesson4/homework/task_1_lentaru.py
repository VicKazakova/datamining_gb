from lxml import html
import requests
import re
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('127.0.0.1', 27017)
db = client['news']

db_news = db.db_news

headers = \
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/96.0.4664.110 Safari/537.36'}

response = requests.get('https://lenta.ru/', headers=headers)
dom = html.fromstring(response.text)

final_news = []

big_news = dom.xpath("//div[@class='topnews']")
for i in big_news:
    news = {}
    source = 'lenta.ru'
    name = ''.join(i.xpath(".//h3[@class='card-big__title']/text()"))
    link = 'https://lenta.ru' + ''.join(i.xpath(".//h3[@class='card-big__title']/../../@href"))
    time = ''.join(i.xpath(".//time[@class='card-big__date']//text()"))
    date = ''.join(re.findall(r'\d{4}/\d{2}/\d{2}', link))

    news['_id'] = f'{time}: {name}'
    news['name'] = name
    news['source'] = source
    news['link'] = link
    news['date'] = date
    news['time'] = time
    final_news.append(news)

    try:
        db_news.insert_one(news)
    except DuplicateKeyError:
        pass

items = dom.xpath("//a[contains(@class,'card-mini _topnews')]")  # containers
for small_news in items:
    news = {}
    source = 'lenta.ru'
    name = ''.join(small_news.xpath(".//span[@class='card-mini__title']/text()"))
    initial_link = ''.join(small_news.xpath(".//span[@class='card-mini__title']/../../@href"))
    if initial_link[0] == '/':
        link = 'https://lenta.ru' + initial_link
        date = ''.join(re.findall(r'\d{4}/\d{2}/\d{2}', link))
    else:
        link = initial_link
        date = ''.join(re.findall(r'\d{2}-\d{2}-\d{4}', link)).replace('-', '/')
    time = ''.join(small_news.xpath(".//time[@class='card-mini__date']//text()"))

    news['_id'] = f'{time}: {name}'
    news['name'] = name
    news['source'] = source
    news['link'] = link
    news['date'] = date
    news['time'] = time
    final_news.append(news)

    try:
        db_news.insert_one(news)
    except DuplicateKeyError:
        pass

for doc in db_news.find({}):
    pprint(doc)
