import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib

client = MongoClient('127.0.0.1', 27017)
db = client['posts']
lenta_posts = db.lenta_posts

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'}
url = 'https://lenta.ru'
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

last_24_news_refs = dom.xpath("//div[@class = 'last24']//@href")
main_news_refs = dom.xpath("//div[@class = 'main-container']//a[contains(@class, 'news')]/@href")
last_24_news = []
main_news = []

for i in last_24_news_refs:
    news_item = {}
    news_item['source'] = url
    ref = str(url + i)
    response = requests.get(ref, headers=header)
    dom = html.fromstring(response.text)
    title = dom.xpath("//span[@class='topic-body__title']/text()")
    date = dom.xpath("//a[contains(@class, 'topic-header__time')]/text()")
    news_item['title'] = title
    news_item['ref'] = ref
    str_hash = str(title + date)
    str_hash = bytes(str_hash, encoding='utf-8')
    news_item['_id'] = str_hash
    last_24_news.append(news_item)

for i in main_news_refs:
    main_news_item = {}
    main_news_item['source'] = url
    ref = str(url + i)
    response = requests.get(ref, headers=header)
    dom = html.fromstring(response.text)
    title = dom.xpath("//span[@class='topic-body__title']/text()")
    date = dom.xpath("//a[contains(@class, 'topic-header__time')]/text()")
    main_news_item['title'] = title
    main_news_item['ref'] = ref
    str_hash = str(title + date)
    str_hash = bytes(str_hash, encoding='utf-8')
    main_news_item['_id'] = str_hash
    if main_news_item['title'] != []:
        main_news.append(main_news_item)

pprint(main_news)

for news in last_24_news:
    try:
        lenta_posts.insert_one(news)
    except DuplicateKeyError:
        print(f'item  already exists')

for news in main_news:
    try:
        lenta_posts.insert_one(news)
    except DuplicateKeyError:
        print(f'item  already exists')

for i in lenta_posts.find({}):
    pprint(i)
