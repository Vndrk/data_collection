from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from jobparcer.spiders.hhru import HhruSpider
from jobparcer.spiders.superjob import SuperjobSpider

if __name__ == '__main__':
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    configure_logging()
    process = CrawlerProcess(get_project_settings())
    process.crawl(HhruSpider)
    process.crawl(SuperjobSpider)
    process.start()

