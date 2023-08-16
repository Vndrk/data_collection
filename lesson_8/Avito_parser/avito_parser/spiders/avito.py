import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from avito_parser.items import AvitoParserItem


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["avito.ru"]
    start_urls = ["https://www.avito.ru/moskva?p=100&q=ps5"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 1
        self.start_urls = [f"https://www.avito.ru/moskva?p={self.page}&q={kwargs.get('query')}"]

    def start_requests(self):
        if not self.start_urls and hasattr(self, "start_url"):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            yield SplashRequest(url=url)

    def parse(self, response, **kwargs):
        links = response.xpath("//a[contains(@class, 'item-slider')]/@href").getall()
        if links:
            for link in links:
                yield SplashRequest("https://avito.ru" + link, callback=self.parse_item)
        self.page += 1
        if self.page <= 100 & response.status == 200:
            yield SplashRequest(self.start_urls[0], callback=self.parse)


    def parse_item(response):
        loader = ItemLoader(item=AvitoParserItem(), response=response)
        loader.add_xpath('name', '//span[@class="title-info-title-text"]//text()')
        loader.add_xpath('price', "//span[@itemprop='price']//@content")
        loader.add_xpath('currency', "//span[@itemprop='priceCurrency']//@content")
        loader.add_xpath('photos', "//img[contains(@class, 'desktop')]//@src")
        loader.add_value('url', response.url)
        yield loader.load_item()
