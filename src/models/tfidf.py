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
    return pd.read_csv(DATA_FOLDER + 'preprocessed_data/preprocessed_data.csv')

def train_tfidf(dfs):
    content = dfs['page_content']
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(content)
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    return cosine_similarities


def recommend(cosine_similarities, df, i, n=2):
    indexes = heapq.nlargest(n, range(len(cosine_similarities[i])), cosine_similarities[i].take)[1:]
    return df.loc[indexes, 'url']


def train_and_recommend(article_content):

    corpus = get_data()
    new_data = preprocess(pd.DataFrame({'page_content': [article_content]}))

    corpus = pd.concat([corpus, new_data], ignore_index=True)
    index = corpus.shape[0] - 1

    tf_model = train_tfidf(corpus)
    cos_sim = cosine_similarity(tf_model, tf_model)

    recommendations = recommend(cos_sim, corpus, index)

    return recommendations



#x = get_data(df_list)
#y = train_tfidf(x)
#print(y)