import scrapy
from scrapy.http import HtmlResponse
from castorama_parser.items import CastoramaParserItem
from scrapy.loader import ItemLoader

class CastoramaparserSpider(scrapy.Spider):
    name = 'castoramaparser'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('item')}"]


    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='product-card__img-link']")
        if links:
            for link in links:
                yield response.follow(link, callback=self.parse_item)
        next_page = response.xpath("//a[@title='След.']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response:HtmlResponse):
        loader = ItemLoader(item=CastoramaParserItem(), response=response)
        loader.add_xpath('name',  '//h1/text()')
        loader.add_xpath('price', '//span[@class = "regular-price"]/text()')
        loader.add_xpath('currency', '//span[@class = "currency"]/text()')
        loader.add_xpath('photos', "//ul[@class = 'swiper-wrapper']//li/img/@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()



