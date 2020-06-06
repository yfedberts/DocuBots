from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
import scrapy
import pandas as pd
from items import DocSpiderItem

class DocSpider(scrapy.Spider):
    name = 'doc_spider'

    urlsList = pd.read_csv('B:\docubot\DocuBots\csvFiles\linksToScrape.csv')
    urls = []
    for url in urlsList['urls']:
        urls.append(url)

    start_urls = urls

    def parse(self, response):
        data = {}
        for content in response.xpath('/html//div[@class]//div[@class]//p'):
            if content:
                data['links'] = response.request.url
                data['texts'] = " ".join(content.xpath('//p/text()').extract())
            
        yield data