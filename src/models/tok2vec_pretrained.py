import numpy as np
import spacy
import pandas as pd
import os

global DATA_FOLDER
DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')


def recommend(article):
    nlp = spacy.load('pl_core_news_lg')

    embed_mat = pd.read_pickle(DATA_FOLDER + 'preprocessed_data/embed_mat.pkl')
    embed_mat = embed_mat['page_content'].to_numpy()

    df = pd.read_csv(DATA_FOLDER + 'preprocessed_data/preprocessed_data.csv')
    #df['page_content'] = df['page_content'].apply(lambda x: nlp(x))
    #embed_mat = df['page_content'].values

    query_embed = nlp(article)
    mat = np.array([query_embed.similarity(line) for line in embed_mat])
    index = np.argmax(mat)

    return df.loc[index, 'url']


def save():
    nlp = spacy.load('pl_core_news_lg')

    df = pd.read_csv(DATA_FOLDER + 'preprocessed_data/preprocessed_data.csv')

    df['page_content'] = df['page_content'].apply(lambda x: nlp(x))
    embed_mat = df['page_content'].values
    return embed_mat

if __name__=='__main__':
    save()

