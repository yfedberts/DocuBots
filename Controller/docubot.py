import sys, os
sys.path.append('Controller\search_engine.py')
sys.path.append('Controller\scrapeprocessor.py')
from search_engine import SearchEngine
from scrapeprocessor import ScrapeProcessor
import pandas as pd
import time

class DocuBot():
    def analyze_simi(self, doc):
        start = time.time()
        SE = SearchEngine()
        SP = ScrapeProcessor()
        filename = doc
        lr, se_scores = SE.get_simi_link(filename)
        df = pd.DataFrame()
        df = SP.check_simi()
        df['Search Engine Scores'] = se_scores

        if(os.path.exists(r'B:\docubot\DocuBots\Model\Data\simi_results.csv')):
            os.remove(r'B:\docubot\DocuBots\Model\Data\simi_results.csv')
        df.to_csv(r'B:\docubot\DocuBots\Model\Data\simi_results.csv')

        end = time.time()
        print("Time taken to analyze: {}".format(end-start))
        return df

    def get_current_results(self):
        df = pd.read_csv(r'B:\docubot\DocuBots\Model\Data\simi_results.csv')
        print(df)

DB = DocuBot()
print(DB.analyze_simi(r"B:\docubot\DocuBots\Model\docxFiles\sample.docx"))
df = pd.read_csv(r'B:\docubot\DocuBots\Model\Data\simi_results.csv')
print(df['Individual Similarity Score'])
print(df['Most Similar Content'])
print(df['Total Score'])