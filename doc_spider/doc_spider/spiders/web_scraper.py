from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
import scrapy, os, pandas
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
    urlsList = pandas.read_csv('B:\docubot\DocuBots\Model\Data\linksToScrape.csv')
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
        for content in response.xpath('/html//body//div[@class]//div[@class]//p'):
            if content:
                #Append the current url
                data['links'] = response.request.url
                #Append the texts within the <p> tags
                data['texts'] = " ".join(content.xpath('//p/text()').extract())

        yield data

    def run_crawler(self):
        try:
            os.path.exists("scrape_results.json")
            os.remove("scrape_results.json")
            ds = DocSpider()
            ds.run_crawler()
        except:
            if __name__ ==  "__main__":
                settings = get_project_settings()
                settings.set('FEED_FORMAT', 'json')
                settings.set('FEED_URI', 'scrape_results.json')
                c = CrawlerProcess(settings)
                c.crawl(DocSpider)
                c.start(stop_after_crawl=True)

ds = DocSpider()
ds.run_crawler()