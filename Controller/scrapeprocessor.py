import pandas as pd
import os, json
from Controller.article_crawler.run_scraper import Scraper
from doc_reader import DocReader
import time
from nltk.corpus import wordnet as wn

CURR_PATH = os.path.dirname(__file__)
DATA_FOLDER = os.path.relpath("..\\Model\\Data")

DOC_TEXTS = os.path.join(CURR_PATH, DATA_FOLDER, "doc_texts.csv")
LINKS_LIST = os.path.join(CURR_PATH, DATA_FOLDER, "linksToScrape.csv")
SCRAPE_RESULTS_CSV = os.path.join(CURR_PATH, DATA_FOLDER, "scrape_results.csv")
SCRAPE_RESULTS_JSON = os.path.join(CURR_PATH, DATA_FOLDER, "scraped_results.json")

class ScrapeProcessor():

    def clean_text(self, filename):
        with open(filename) as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        df['content'] = df['content'].astype(str).str.strip(r'\r').str.strip(r'\xa0').str.strip(r'\n').str.strip(r'\t')
        df.to_csv(SCRAPE_RESULTS_CSV, encoding='utf-8-sig')

    def scrape_links(self):
        if(os.path.exists(SCRAPE_RESULTS_CSV)):
            os.remove(SCRAPE_RESULTS_CSV)
        scraper = Scraper()
        scraper.run_spider()
        self.clean_text(SCRAPE_RESULTS_JSON)

    def web_doc_similarity(self):
        start = time.time()
        df = pd.read_csv(DOC_TEXTS)
        df2 = pd.read_csv(SCRAPE_RESULTS_CSV)

        dr = DocReader()
        #Convert to Synsets
        webSynSets = []
        docSynSets = []
        for r, t in zip(df2.content.tolist(),df.ParaText.tolist()):
            webSynSets.append(dr.str_to_synsets(str(r)))
            docSynSets.append(dr.str_to_synsets(str(t)))

        result_scores = 0.0
        indiv_scores = []
        simi_content = []
        simi_links = []

        for ss1 in docSynSets:
            docsets = ss1
            best_score = 0.0
            best_content = ""
            best_link = ""
            ss2_num = 0
            it = 0
            for ss2 in webSynSets:
                websets = ss2
                simi = dr.quick_compare(docsets,websets)
                print(simi)
                if(simi > 0.01):
                    if(simi > best_score):
                            best_score = simi
                            best_content = df2.loc[it, 'content']
                            best_link = df2.loc[it, 'url']
                            ss2_num = it
                it+=1
            if best_score > 0.0:
                del webSynSets[ss2_num]

            indiv_scores.append(best_score)
            result_scores += best_score

            simi_links.append(best_link)
            simi_content.append(best_content)

        end = time.time()
        print(end-start)
        try:
            return indiv_scores, simi_links, simi_content
        except:
            return 0.0, 0.0, "None Found", "None Found"

    def check_simi(self):
        sp = ScrapeProcessor()
        sp.scrape_links()
        indiv_scores, simi_links, simi_content  = self.web_doc_similarity()
        df = pd.DataFrame()
        df['simi_links'] = pd.Series(simi_links)
        df['simi_content'] = pd.Series(simi_content)
        df['indiv_scores'] = indiv_scores

        return df