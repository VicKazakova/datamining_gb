import unicodedata

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

response = requests.get('https://news.mail.ru/', headers=headers)
dom = html.fromstring(response.text)

big_news = dom.xpath("//a[contains(@class, 'js-topnews')]")
small_news = dom.xpath("//li[contains(@class, 'list__item')]")

for i in big_news:
    news = {}
    name = unicodedata.normalize("NFKD", ''.join(
        i.xpath(".//span[@class='photo__title photo__title_new photo__title_new_hidden "
                "js-topnews__notification']/text()")))
    link = ''.join(i.xpath(".//span[@class='photo__title photo__title_new photo__title_new_hidden "
                           "js-topnews__notification']/../../@href"))
    internal_response = requests.get(link, headers=headers)
    internal_dom = html.fromstring(internal_response.text)
    source = ''.join(internal_dom.xpath("//a[@class='link color_gray breadcrumbs__link']/span/text()"))
    time = ''.join(internal_dom.xpath("//span[contains(@datetime, '-') "
                                      "and contains(@class, 'note__text')]/text()")).replace('(мск)', '')
    date = ''.join(internal_dom.xpath("//span[contains(@datetime, '-') "
                                      "and contains(@class, 'note__text')]/@datetime")).split('T')[0].replace('-', '/')
    news['_id'] = f'{time}: {name}'
    news['name'] = name
    news['source'] = source
    news['link'] = link
    news['date'] = date
    news['time'] = time
    # print(news)

for i in small_news:
    news = {}
    link = ''.join(i.xpath(".//a[@class='list__text']/@href"))
    if link != '':
        name = unicodedata.normalize("NFKD", ''.join(i.xpath(".//a[@class='list__text']/text()")))
        internal_response = requests.get(link, headers=headers)
        internal_dom = html.fromstring(internal_response.text)
        source = ''.join(internal_dom.xpath("//a[@class='link color_gray breadcrumbs__link']/span/text()"))
        time = ''.join(internal_dom.xpath("//span[contains(@datetime, '-') "
                                          "and contains(@class, 'note__text')]/text()")).replace('(мск)', '')
        date = ''.join(internal_dom.xpath("//span[contains(@datetime, '-') "
                                          "and contains(@class, 'note__text')]/@datetime")).split('T')[0].replace('-',
                                                                                                                  '/')
        news['_id'] = f'{time}: {name}'
        news['name'] = name
        news['source'] = source
        news['link'] = link
        news['date'] = date
        news['time'] = time

        if not news:
            pass
        else:
            try:
                db_news.insert_one(news)
            except DuplicateKeyError:
                pass

for doc in db_news.find({}):
    pprint(doc)
