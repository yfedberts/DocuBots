import sys, os
sys.path.append(r'Controller\search_engine.py')
sys.path.append(r'Controller\scrapeprocessor.py')
from Controller.search_engine import SearchEngine
from Controller.scrapeprocessor import ScrapeProcessor
from doc_reader import DocReader
import pandas as pd
import time

class DocuBot():

    THRESH = 0.0

    doc = ""
    doc_local = ""
    doc_reader = DocReader()

    def __init__(self):
        self.THRESH = 0.5

    #SET FUNCTIONS
    def set_file_path(self, filename, option):
        if(filename.lower().endswith('.docx') and os.path.isfile(filename)):
            if(option == 1):
                self.doc = filename

                if self.doc is not None:
                    print("File uploaded successfully")
                    return True

            #TODO: SET LOCAL FILES
            if(option == 2):
                self.doc_local = filename
                if self.doc_local is not None:
                    print("File 2 uploaded successfully")
                    return True
        else:
            print("Error: File type not supported please make sure that the file is a .docx file")
            return False

    def set_thresh(self, x):
        sens = [0, 0.1, 0.5, 0.70]
        if((x > 0) and (x < 4)):
            self.THRESH = sens[x]
            print(self.THRESH)

    #GET FUNCTIONS
    def get_thresh(self):
        return self.THRESH

    #RUN ANALYZE
    def merge_dupli(self, data):
        dataset = data
        data_links = dataset.groupby(['simi_links', 'simi_content'])['indiv_scores'].sum().reset_index()
        rows = data_links['indiv_scores'].count()
        score_sum = (data_links['indiv_scores'].astype(int))/rows
        print(data_links)
        print(score_sum)
        return score_sum

    def analyze_simi_online(self):

        if(os.path.exists(r'B:\docubot\DocuBots\Model\Data\simi_results.csv')):
            os.remove(r'B:\docubot\DocuBots\Model\Data\simi_results.csv')

        start = time.time()
        filename = self.doc
        se = SearchEngine()
        lr = se.get_simi_link(filename)
        sp = ScrapeProcessor()
        df = sp.check_simi()
        #df['Search Engine Scores'] = se_scores

        indiv_scores = df["indiv_scores"].astype(str).astype(float)
        scoreList = []
        for iscore in indiv_scores:
            scoreList.append(iscore)

        total_score = 0.0
        for score in scoreList:
            if(score > self.THRESH):
                total_score += score

        row_num = len(scoreList)
        output = (total_score/row_num)*100

        df.to_csv(r'B:\docubot\DocuBots\Model\Data\simi_results.csv')
        end = time.time()
        print("Time taken to analyze: {}".format(end-start))
        return output

    def analyze_simi_local(self, d1, d2):
        return self.doc_reader.doc_similarity(d1,d2)

    def test_funct(self):
        data = pd.read_csv(r"B:\docubot\DocuBots\Model\Data\simi_results.csv")
        data_links = data.groupby(['simi_links', 'simi_content'])['indiv_scores'].sum().reset_index()
        rows = data_links['indiv_scores'].count()
        print(data_links)
        print((data_links['indiv_scores'].astype(int))/rows)

dbot = DocuBot()
dbot.test_funct()