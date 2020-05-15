import requests
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
from nltk import word_tokenize
from docx import Document
import analyzer

class SearchEngine():        

    def getQuery(self, filename):
        doc = Document(filename)
        fullText = ''
        for p in doc.paragraphs:
            if p != '':
                Text = (p.text)
                fullText += (Text + " ")
        
        return fullText

    def searchWeb(self, queryInput):
        load_dotenv(find_dotenv())

        API_KEY = os.getenv("API_KEY")
        SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
        
        query = queryInput
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        data = requests.get(url).json()

        results_item = data.get("items")

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
                    titles.append(title)
                    snippets.append(snippet)
                    html_snippets.append(html_snippet)
                    links.append(link)
            except:
                continue

        best_score = 0.0
        best_link = ''

        for i, j in zip(snippets,links):
            simi = analyzer.query_similarity(i, query)
            if(simi > best_score):
                best_score = simi
                best_link = j

        return best_link, best_score

    def get_simi_link(self, d):
            
        se = SearchEngine()
        doc = se.getQuery(d)
        link_result, score = se.searchWeb(doc)
        try:
            if(link_result != ''):
                return link_result, score
        except:
            return "No similar content found online"

a = SearchEngine()
print(a.get_simi_link('docxFiles\sample.docx'))