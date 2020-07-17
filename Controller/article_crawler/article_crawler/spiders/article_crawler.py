import pandas as pd
from bs4 import BeautifulSoup as bs4
import scrapy, os
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from doc_reader import DocReader
from pathlib import Path

CURR_PATH = Path(__file__).parents[3]
DATA_FOLDER = os.path.relpath("..\\Model\\Data")
LINKS_LIST = os.path.join(CURR_PATH, DATA_FOLDER, "linksToScrape.csv")

class ArticleCrawler(scrapy.Spider):
    name = 'article_crawler'

    urlLists = []
    df = pd.read_csv(LINKS_LIST)
    for url in df['urls']:
        urlLists.append(url)

    start_urls = urlLists

    def parse(self, response):
        try:
            soup = bs4(response.text, 'lxml')
            charLimit = 10
            scraped_contents = soup.find_all('p')
            tempList = [c.text for c in scraped_contents if c]
            textsList = tempList[0:charLimit]
            contents = " ".join(textsList)
            yield{
                "url": response.url,
                "content": contents
            }
        except:
            yield None