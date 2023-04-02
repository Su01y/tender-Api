import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from nltk import pos_tag
# from nltk.tokenize import word_tokenize
import pymorphy2


df = pd.read_excel('kpgz.xlsx')
column = df['Column2']
categories = column.to_list()
morph = pymorphy2.MorphAnalyzer()


def nouns_only(text):
    text = text.replace(',', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('.', ' ')
    words = text.split()
    nouns = []
    for word in words:
        parsed = morph.parse(word)[0]
        if parsed.tag.POS == 'NOUN' or parsed.tag.POS == 'ADJF':
            normal_word = parsed.normal_form
            nouns.append(normal_word)
    return nouns


nouns_cat = []
for cat in categories:
    nouns_cat.append(nouns_only(cat))

df['noun'] = nouns_cat
print(df.head())

df.to_excel('kpgz.xlsx', index=False)