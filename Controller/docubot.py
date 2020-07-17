import sys, os
sys.path.append(r'Controller\search_engine.py')
sys.path.append(r'Controller\scrapeprocessor.py')
from Controller.search_engine import SearchEngine
from Controller.scrapeprocessor import ScrapeProcessor
from doc_reader import DocReader
import pandas as pd
import time

CURR_PATH = os.path.dirname(__file__)
DATA_FOLDER = os.path.relpath("..\\Model\\Data")
SIMI_RESULT = os.path.join(CURR_PATH, DATA_FOLDER, "simi_results.csv")

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

    #GET FUNCTIONS
    def get_thresh(self):
        return self.THRESH

    #RUN ANALYZE
    def merge_duplicates(self, data):
        #FIX THIS MERGE PART
        try:
            dataset = data.to_frame()
        except:
            dataset = data
        merged_dataset = dataset.groupby(['simi_links', 'simi_content'])['indiv_scores'].mean().reset_index()
        return merged_dataset

    def analyze_simi_online(self):

        if(os.path.exists(SIMI_RESULT)):
            os.remove(SIMI_RESULT)

        start = time.time()
        filename = self.doc
        se = SearchEngine()
        se.get_simi_link(filename)
        sp = ScrapeProcessor()
        df = sp.check_simi()

        clean_df = self.merge_duplicates(df)
        indiv_scores = clean_df['indiv_scores'].astype(str).astype(float)

        scoreList = []
        for iscore in indiv_scores:
            scoreList.append(iscore)

        total_score = 0.0
        url_list = []
        for link, score in zip(clean_df['simi_links'].astype(str), scoreList):
            if(score > self.THRESH):
                total_score += score
                url_list.append(link)

        clean_df.to_csv(SIMI_RESULT)

        try:
            output = (total_score / len(url_list)) * 100
            return output, url_list

        except:
            return 0.0, ["None Found"]

        end = time.time()
        print("Time taken to analyze: {}".format(end-start))

    def analyze_simi_local(self, d1, d2):
        return self.doc_reader.doc_similarity(d1,d2)