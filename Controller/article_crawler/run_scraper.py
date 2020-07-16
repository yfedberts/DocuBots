from Controller.article_crawler.article_crawler.spiders.article_crawler import ArticleCrawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

class Scraper:

    def __init__(self):
        settings_file_path = 'Controller.article_crawler.article_crawler.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = ArticleCrawler

    def run_spider(self):
        if(os.path.exists(r'B:\docubot\DocuBots\Model\Data\scraped_results.json')):
            os.remove(r'B:\docubot\DocuBots\Model\Data\scraped_results.json')

        #if __name__ ==  "__main__":
        self.process.crawl(self.spider)
        self.process.start()