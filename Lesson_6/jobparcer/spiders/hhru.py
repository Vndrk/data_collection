import scrapy
from scrapy.http import HtmlResponse
from jobparcer.items import JobparcerItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=python&salary=&ored_clusters=true&area=1002',
                  "https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=python&ored_clusters=true&L_save_area=true"]

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[@data-qa = 'pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


        links = response.xpath("//a[@class = 'serp-item__title']/@href").getall()
        for link in links:
           yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@data-qa = 'vacancy-title']//text()").get()
        salary = response.xpath("//div[@data-qa = 'vacancy-salary']/span//text()").getall()
        url = response.url
        yield JobparcerItem(name=name, salary=salary, url=url)









