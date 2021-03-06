import pandas as pd
import numpy as np
import os
import heapq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

from src.preprocessing.preprocessing import preprocess

global DATA_FOLDER
DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')


def get_data():
    df = pd.read_csv(DATA_FOLDER + 'preprocessed_data/preprocessed_data.csv')
    return df[~df['page_content'].isna()]


def train_tfidf(dfs):
    content = dfs['page_content']
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(content)
    #cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    return tfidf, tfidf_matrix


def recommend(cosine_similarities, df, i, n=2):
    indexes = heapq.nlargest(n, range(len(cosine_similarities[i])), cosine_similarities[i].take)[1:]
    return df.loc[indexes, 'url']


def train_and_recommend(article_content):

    corpus = get_data()

    #corpus = pd.concat([corpus, article_content], ignore_index=True)
    #index = corpus.shape[0] - 1

    tfidf_model, tfidf_matrix = train_tfidf(corpus)
    
    new_data = tfidf_model.transform([article_content.loc[0,'page_content']])
    #cos_sim = cosine_similarity(tf_model, tf_model)

    #recommendations = recommend(cos_sim, corpus, index)
    z = [cosine_similarity(i,new_data) for i in tfidf_matrix]
    index = z.index(max(z))

    return corpus.loc[index, 'url']



#x = get_data(df_list)
#y = train_tfidf(x)
#print(y)
