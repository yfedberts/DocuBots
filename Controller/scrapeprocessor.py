import pandas as pd
import os, json
from Controller.article_crawler.run_scraper import Scraper
from doc_reader import DocReader

class ScrapeProcessor():
    def clean_text(self, filename):
        with open(filename) as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        df['content'] = df['content'].astype(str).str.strip(r'\\r').str.strip(r'\\xa0').str.strip(r'\\n').str.strip(r'\\t')
        df.to_csv(r'Model\Data\scrape_results.csv', encoding='utf-8-sig')


    def scrape_links(self):
        sp = ScrapeProcessor()
        if(os.path.exists(r'Model\Data\scrape_results.csv')):
            os.remove(r'Model\Data\scrape_results.csv')
        scraper = Scraper()
        scraper.run_spider()
        sp.clean_text(r'Model\Data\scraped_results.json')

    def web_doc_similarity(self):
        df = pd.read_csv(r'B:\docubot\DocuBots\Model\Data\doc_texts.csv')
        df2 = pd.read_csv(r'B:\docubot\DocuBots\Model\Data\scrape_results.csv')

        dr = DocReader()
        #Convert to Synsets
        webSynSets = []
        docSynSets = []
        for r in df2.content.tolist():
            webSynSets = [dr.str_to_synsets(str(r))]

        for t in df.ParaText.tolist():
            docSynSets = [dr.str_to_synsets(str(t))]

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
                if(simi > 0.01):
                    if(simi > best_score):
                            best_score = simi
                            best_content = df2.loc[it, 'content']
                            best_link = df2.loc[it, 'url']
                            ss2_num = it
                    else:
                        continue
                it+=1

            if(best_score == 0.0):
                del(webSynSets[ss2_num])

            indiv_scores.append(best_score)
            simi_links.append(best_link)
            simi_content.append(best_content)
            result_scores += best_score

        return((result_scores/len(simi_content)) * 100), indiv_scores, simi_links, simi_content

    def check_simi(self):
        sp = ScrapeProcessor()
        total_score, indiv_scores, simi_links, simi_content  = sp.web_doc_similarity()
        df = pd.DataFrame()
        df['Similar Links'] = simi_links
        df['Most Similar Content'] = simi_content
        df['Individual Similarity Score'] = indiv_scores
        df['Total Score'] = total_score
        df.to_csv(r'B:\docubot\DocuBots\Model\Data\simi_results.csv')