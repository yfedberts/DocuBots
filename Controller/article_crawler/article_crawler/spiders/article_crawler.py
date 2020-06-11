import pandas as pd
from bs4 import BeautifulSoup as bs4
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from doc_reader import DocReader

class ArticleCrawler(scrapy.Spider):
    name = 'article_crawler'

    urlLists = []
    df = pd.read_csv(r'B:\docubot\DocuBots\Model\Data\linksToScrape.csv')
    for url in df['urls']:
        urlLists.append(url)

    start_urls = urlLists

    def parse(self, response):
        try:
            soup = bs4(response.text, 'lxml')
            scraped_contents = soup.find_all('p')
            texts = [c.text for c in scraped_contents]
            contents = " ".join(texts)
            yield{
                "url": response.url,
                "content": contents
            }
        except:
            yield None