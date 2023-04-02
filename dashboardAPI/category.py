import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from nltk import pos_tag
# from nltk.tokenize import word_tokenize
import pymorphy2
import numpy as np
# import time


df = pd.read_excel('kpgz.xlsx')
categories = df['Column2']
nouns_cat = df['noun']
categories = categories.to_list()
morph = pymorphy2.MorphAnalyzer()


def nouns_only(text):
    text = text.replace(',', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    words = text.split()
    nouns = []
    for word in words:
        parsed = morph.parse(word)[0]
        if parsed.tag.POS == 'NOUN' or parsed.tag.POS == 'ADJF':
            nouns.append(parsed.normal_form)
    return nouns


def categorize(service):
    # print('start', time.time())
    category = service
    nouns_s = nouns_only(service)
    max_cos = 0
    # print('med', time.time())
    for n, c in zip(nouns_cat, categories):
        n = n.replace('[', ' ')
        n = n.replace(']', ' ')
        n = n.replace("'", ' ')
        n = n.replace(',', ' ')        
        n = n.split()
        
        set1 = set(nouns_s)
        set2 = set(n)
        total_set = set1 | set2
        vector1 = np.array([nouns_s.count(word) for word in total_set])
        vector2 = np.array([n.count(word) for word in total_set])

        cos = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

        if cos > max_cos:
            category = c
            max_cos = cos
    # print('end', time.time())
    return category