import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
db_mvideo = db.db_mvideo

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='../classwork/chromedriver', options=options)
driver.get('https://www.mvideo.ru/')

# close all useless banners:
button = driver.find_element(By.XPATH, "//button[contains(@class,'insider-banner-close-button')]")
button.click()
button = driver.find_element(By.XPATH, "//mvid-icon[contains(@class,'location-close-icon')]")
button.click()

driver.execute_script("window.scrollTo(0, 1160)")
time.sleep(10)

names = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-mini-card__name')]")
links = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-mini-card__name')]/div/a")
prices = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-mini-card__price')]")
new_prices = []
old_prices = []
for i in prices:
    new_price = i.find_element(By.XPATH, "//span[@class='price__main-value' and ancestor::div[contains(@class, "
                                         "'product-mini-card__price')]]").text
    new_prices.append(new_price)
    try:
        old_price = i.find_element(By.XPATH, "//span[@class='price__sale-value' and ancestor::div[contains(@class, "
                                             "'product-mini-card__price')]]").text
        old_prices.append(old_price)
    except Exception:
        old_price = None
        old_prices.append(old_price)
ratings_feedbacks = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-mini-card__rating')]")

for j in range(0, len(names)):
    mvideo_data = {'_id': names[j].text,
                   'link': links[j].get_attribute('href'),
                   'new_price': new_prices[j],
                   'old_price': old_prices[j],
                   'rating': ratings_feedbacks[j].text[:3],
                   'feedback': ratings_feedbacks[j].text[4:]
                   }
    try:
        db_mvideo.insert_one(mvideo_data)
    except DuplicateKeyError:
        pass

for doc in db_mvideo.find({}):
    pprint(doc)

driver.quit()
