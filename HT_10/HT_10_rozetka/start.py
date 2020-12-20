from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':

    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl('rozetka')
    crawler.start()
