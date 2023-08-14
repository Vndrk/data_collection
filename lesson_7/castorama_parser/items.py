# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst

def process_price(price):
    try:
        price = int(price[2].replace(' ', ''))
    except:
        pass
    return price

def process_photos(photo):
    photos = ["https://castorama.ru" + photo for photo in photos if photo[0] == "/"]
    return photos




class CastoramaParserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photos))
    url = scrapy.Field(output_processor=TakeFirst())






