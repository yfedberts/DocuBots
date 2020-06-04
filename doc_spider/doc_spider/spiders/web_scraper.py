from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
import scrapy

class DocSpider(scrapy.Spider):
    name = 'doc_spider'
    start_urls = ['https://www.newyorker.com/magazine/2020/01/13/the-future-of-americas-contest-with-china']

    def parse(self, response):
        for desc in response.xpath('/html//div[@class]//div[@class]//p'):
            if desc:
                test = desc.xpath('//p/text()').extract()
        
        yield{  
            'test': test
        }


