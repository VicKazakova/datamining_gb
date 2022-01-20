# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для
# парсинга использовать XPath. Структура данных должна содержать: название источника; наименование новости; ссылку на
# новость; дата публикации. Сложить собранные новости в БД

from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news']


