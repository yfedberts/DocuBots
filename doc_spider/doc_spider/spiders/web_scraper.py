from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
import scrapy

class DocSpider(scrapy.Spider):
    name = 'doc_spider'
    start_urls = ['https://www.placepass.com/blog/ultimate-travel-bucket-list']

    def parse(self, response):
        for desc in response.xpath('/html//div[@class]//div[@class]//p'):
            if desc:
                test = desc.xpath('//p/text()').extract()
        
        yield{  
            'test': test
        }


