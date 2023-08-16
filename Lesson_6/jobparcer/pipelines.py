# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import regex

class JobparcerPipeline:
    def __int__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy


    def process_item(self, item, spider):

        collection = self.mongo_base[spider.name]
        upd_item = self.update_item(item)
        collection.insert_one(item)
        return upd_item

    def update_item(self, item):
        upd_item = item.deepcopy()
        del upd_item['salary']
        upd_item['min_salary'] = None
        upd_item['max_salary'] = None
        upd_item['cur'] = None
        if item['salary']:
            salary = [s.replace(u'\xa0', '') for s in item['salary']]
            for ind, s in  enumerate(salary):
                if s.isdigit():
                    if salary[ind - 1].strip() == 'от':
                        upd_item['min_salary'] = int(s)
                    elif salary[ind - 1].strip() == 'до':
                        upd_item['max_salary'] = int(s)
            upd_item['cur'] = regex.findall(r'\p{Sc}', "".join(item['salary']))[0]
        return upd_item
