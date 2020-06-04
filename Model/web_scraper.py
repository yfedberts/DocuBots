"""
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd

df = pd.read_csv("csvFiles/linksToScrape.csv")
links = df['urls'].tolist()

content = []
scrapeUrl = "https://www.metmuseum.org/exhibitions/listings/2019/home-is-a-foreign-place"

req = Request(scrapeUrl, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

print(webpage)

page_soup = soup(webpage, "html.parser")
containers = page_soup.findAll("p")
for container in containers:
    print(container)
"""