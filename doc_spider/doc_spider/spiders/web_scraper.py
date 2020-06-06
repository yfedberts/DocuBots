from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
import scrapy
import pandas as pd
from items import DocSpiderItem

class DocSpider(scrapy.Spider):
    """
    This is the broad scraper, the name is doc_spider and can be invoked by making an object
    of the CrawlerProcess() then calling the class of the Spider. It scrapes websites csv file
    for the content and returns the results as a .json file.
    """

    #Name of Spider
    name = 'doc_spider'

    #File of the URL list here
    urlsList = pd.read_csv('B:\docubot\DocuBots\csvFiles\linksToScrape.csv')
    urls = []
    #Take the urls and insert them into a url list
    for url in urlsList['urls']:
        urls.append(url)

    #Scrape through all the websites in the urls list
    start_urls = urls

    #This method will parse the results and will be called automatically
    def parse(self, response):
        data = {}
        #Iterates through all <p> tags
        for content in response.xpath('/html//div[@class]//div[@class]//p'):
            if content:
                #Append the current url
                data['links'] = response.request.url
                #Append the texts within the <p> tags
                data['texts'] = " ".join(content.xpath('//p/text()').extract())

        yield data