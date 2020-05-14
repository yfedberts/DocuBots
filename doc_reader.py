from docx import Document
from nltk import word_tokenize, sent_tokenize
import pandas as pd
    
def getQuery(filename):
    doc = Document(filename)
    fullText = []
    for p in doc.paragraphs:
        if p.text != '':
            fullText.append(p.text)
    return fullText

df = pd.DataFrame()    
df['WORDS'] = getQuery(r'docxFiles\sample.docx')
df.to_csv(r'csvFiles\query.csv')
