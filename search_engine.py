import requests
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
from nltk import word_tokenize

class SearchEngine():        

    def searchWeb(self, queryInput):
        load_dotenv(find_dotenv())

        API_KEY = os.getenv("API_KEY")
        SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
        
        query = queryInput
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"

        data = requests.get(url).json()

        results_item = data.get("items")
        
        similarity = 0;
        titles = []
        snippets = []
        html_snippets = []
        links = []

        for i, results_item in enumerate(results_item, start=1):
            try:
                title = results_item.get("title")
                snippet = results_item.get("snippet")
                html_snippet = results_item.get("htmlSnippet")
                link = results_item.get("link")

                if(title != '' and snippet != '' and html_snippet != '' and link != ''):
                    print("="*10, f"Result #{i}", "="*10)
                    print("Title: ", title)
                    print("Description: ", snippet)
                    print("HtmlDescription: ", html_snippet)
                    print("URL: ", link, "\n")

                    titles.append(title)
                    snippets.append(snippet)
                    html_snippets.append(html_snippet)
                    links.append(link)
            except:
                continue
        
        df = pd.DataFrame()
        df['Title'] = titles
        df['Descriptions'] = snippets
        df['Html Snippets'] = html_snippets
        df['Links'] = links
        df['Query'] = query
        df.to_csv(r'csvFiles\google.csv')

        return titles, snippets, links, query

    def getResults(self):
        try:
            queryFile = open(r"csvFiles\query.csv")
            titles = []
            descs = []
            links = []
            queries = []
            if(queryFile):
               data =  pd.read_csv(r"csvFiles\query.csv")

               for w in data['WORDS']:
                   se = SearchEngine()
                   title, desc, link, query = se.searchWeb(w)
                   titles.append(title)
                   descs.append(desc)
                   links.append(link)
                   queries.append(query)
            
            data['Title'] = titles
            data['Descriptions'] = descs
            data['Links'] = links
            data['Query'] = queries
            data.drop(['Unnamed: 0'], axis = 1)
            data.to_csv('csvFiles\results.csv')

        except IOError:
            print("File not found, please input a document to check first")

a = SearchEngine()
a.getResults()