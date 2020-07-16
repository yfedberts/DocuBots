import requests
import os
from dotenv import load_dotenv, find_dotenv
from nltk import word_tokenize, sent_tokenize
from docx import Document
import doc_reader
import pandas as pd

class SearchEngine():

    def searchWeb(self, qInput):
        """
        Function to search the web using paragraphs from the docx files as a query, returning at most 10 results for each paragraphs,
        It then compares each results with query and returns only the most similar result
        """

        #Read the .env files to get API Key and Search engine ID
        load_dotenv(find_dotenv())
        API_KEY = os.getenv("API_KEY4")
        SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

        #Create an object of the doc_reader class to compare similarities
        dr = doc_reader.DocReader()

        #Initiale lists that stores paragraphs for queries, most similar links, and total score respectively
        queryInput = qInput
        result_links = []
        result_scores = 0.0

        #Iteratively finds best results for each paragraphs in the document
        for q in range(len(queryInput)):
            query = queryInput[q]
            url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
            data = requests.get(url).json()

            #Get the results returned from the search engine
            results_item = data.get("items")
            #If empty then skip
            if results_item == None:
                continue
            snippets = []
            links = []

            #Appends link and descriptions from the search results into a list
            for rs in results_item:
                try:
                    snippet = rs.get("snippet")
                    link = rs.get("link")

                    snippets.append(snippet)
                    links.append(link)
                except:
                    continue

            #Temp variable to store highest similarity and most similar link
            best_score = 0.0
            best_link = ''

            #Iterate through the descriptions and compare with query
            #Replace current best if score is higher than the current best
            for i in range(len(snippets)):
                simi = dr.query_similarity(snippets[i], query)
                if(simi > best_score):
                    best_score = simi
                    if(".pdf" not in links[i] and ".PDF" not in links[i]):
                        best_link = links[i]

            result_links.append(best_link)
            result_links = [rs for rs in result_links if rs]
            result_scores += best_score

        #Returns the total score and most similar links to each paragraphs
        try:
            return((result_scores/len(result_links)) * 100), result_links
        except:
            return 0.0, None

    def get_simi_link(self, d):

        """
        Take in a document file and find the most similar contents online
        Based on the content of each paragraphs
        """

        dr = doc_reader.DocReader()
        se = SearchEngine()
        doc = dr.getQuery(d)
        score, links_result = se.searchWeb(doc)
        df = pd.DataFrame()
        print(links_result)
        df['urls'] = links_result
        #EDIT THIS
        df.to_csv(r"B:\docubot\DocuBots\Model\Data\linksToScrape.csv")
        try:
            if(links_result != '' and score != 0.0):
                return links_result, score
        except:
            return "No similar content found online"