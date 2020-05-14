from nltk import word_tokenize, sent_tokenize, pos_tag
import nltk
import statistics
from docx import Document
from nltk.corpus import wordnet as wn

def tag_conversion(penntag):
    morphy_tag = {'NN':wn.NOUN, 'JJ':wn.ADJ,
                  'VB':wn.VERB, 'RB':wn.ADV}
    try:
        return morphy_tag[penntag[:2]]
    except KeyError:
        return None

def doc_to_synsets(doc):
    
    token = nltk.word_tokenize(doc)
    tag = nltk.pos_tag(token)
    wn_tag = [(i[0], tag_conversion(i[1])) for i in tag]
    output = [wn.synsets(i, z)[0] for i, z in wn_tag if len(wn.synsets(i, z))>0]
    print(output)
    return output

def similarity_ratio(s1,s2):
    testList = []

    for s in s1:
        testList.append(max([i.path_similarity(s) for i in s2 if i.path_similarity(s) is not None]))
        if(i.path_similarity(s) for i in s2 if i.path_similarity(s) is None):
            return 0

    output = sum(testList)/len(testList)
    return output

def analyze_similarity(d1, d2):

    synsets1 = doc_to_synsets(d1)
    synsets2 = doc_to_synsets(d2)

    return(similarity_ratio(synsets1,synsets2) + similarity_ratio(synsets2, synsets1)) /2

