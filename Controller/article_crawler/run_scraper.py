from Controller.article_crawler.article_crawler.spiders.article_crawler import ArticleCrawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


CURR_PATH = os.path.dirname(__file__)
DATA_FOLDER = os.path.relpath("..\\Model\\Data")
SCRAPE_RESULTS_JSON = os.path.join(CURR_PATH, DATA_FOLDER, "scraped_results.json")

class Scraper:

    def __init__(self):
        settings_file_path = 'Controller.article_crawler.article_crawler.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = ArticleCrawler
        self.process.start()

    def run_spider(self):
        if(os.path.exists(SCRAPE_RESULTS_JSON)):
            os.remove(SCRAPE_RESULTS_JSON)

        #if __name__ ==  "__main__":
        self.process.crawl(self.spider)