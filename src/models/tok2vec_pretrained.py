import numpy as np
import spacy
import pandas as pd
import os

from src.preprocessing.preprocessing import preprocess

global DATA_FOLDER
DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')


def recommend(article):
    nlp = spacy.load('pl_core_news_md',  disable=['morphologizer',
                                                  'parser',
                                                  'lemmatizer',
                                                  'tagger',
                                                  'senter',
                                                  'attribute_ruler',
                                                  'ner'])

    #preprocessing input
    article_df = preprocess(pd.DataFrame({'page_content': [article]}))
    article_preprocessed = article_df.loc[0, 'page_content']

    df = pd.read_csv(DATA_FOLDER + 'preprocessed_data/preprocessed_data.csv')
    df = df[~df['page_content'].isna()]
    df['page_content'] = df['page_content'].apply(lambda x: nlp(x))
    embed_mat = df['page_content'].values

    query_embed = nlp(article_preprocessed)
    mat = np.array([query_embed.similarity(line) for line in embed_mat])
    index = np.argmax(mat)

    return df.loc[index, 'url']


def save():
    nlp = spacy.load('pl_core_news_lg')

    df = pd.read_csv(DATA_FOLDER + 'preprocessed_data/preprocessed_data.csv')
    df = df[~df['page_content'].isna()]

    df['page_content'] = df['page_content'].apply(lambda x: nlp(x))
    embed_mat = df['page_content'].values

    df = pd.DataFrame({"page_content": embed_mat})
    df.to_pickle(DATA_FOLDER + 'preprocessed_data/embed_mat.pkl')
    return embed_mat


"""if __name__=='__main__':
    save()
    print('go')"""

