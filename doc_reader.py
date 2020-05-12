from docx import Document
from nltk import word_tokenize
import pandas as pd
    
def getText(filename):
    doc = Document(filename)
    fullText = []
    for p in doc.paragraphs:
        tokenized = word_tokenize(p.text)
        fullText.append(tokenized)
    return fullText

df = pd.DataFrame()    
df['WORDS'] = getText('sample.docx')
df.to_csv('query.csv')