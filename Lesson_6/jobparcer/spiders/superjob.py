import scrapy
from scrapy.http import HtmlResponse
from jobparcer.items import JobparcerItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[@class = '_1IHWd T8kbs _37aW8 xctf0 f-test-button-dalshe f-test-link-Dalshe']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@class = 'f-test-search-result-item']//@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("////div[@class = 'f-test-search-result-item']//a[contains(@class, '_1IHWd f-test-link')]/text()]").get()
        salary = response.xpath("//div[@class = 'f-test-text-company-item-salary']//text()").getall()
        url = response.url
        yield JobparcerItem(name=name, salary=salary, url=url)
