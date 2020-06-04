from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
import pandas as pd
from items import DocSpiderItem

class DocSpider(CrawlSpider):
    name = 'doc_spider'
    start_urls = ['http://quotes.toscrape.com']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=False),
    )
    
    def parse_item(self, response):
        for quote in response.xpath('//div[@class]//div[@class]//div[@class]'):
            if quote:
                test = quote.xpath('//div[@class]//span/text()').extract_first()
        
        yield{
            'test': test
        }


