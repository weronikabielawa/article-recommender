import numpy as np
import spacy
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity

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

    article_preprocessed = article.loc[0, 'page_content']

    df = pd.read_csv(DATA_FOLDER + 'preprocessed_data/pretrained_spacy.csv')
    query_embed = nlp(article_preprocessed)
    mat = np.array([cosine_similarity(
        [query_embed.vector.tolist()],
        [[float(x) for x in i.replace('\n',' ')[1:-1].split(" ") if x!='']]
    )[0][0] for i in df['vector']])
    index = np.argmax(mat)

    return pd.read_csv(DATA_FOLDER+'preprocessed_data/url.csv').loc[index, 'url']


def save():
    nlp = spacy.load('pl_core_news_md')
    print('go1')
    df = pd.read_csv(DATA_FOLDER + 'preprocessed_data/preprocessed_data.csv')
    df = df[~df['page_content'].isna()]
    print('go2')
    df['page_content'] = df['page_content'].apply(lambda x: nlp(x))
    df['vector'] = df['page_content'].apply(lambda x: x.vector)
    print('go3')
    #df = pd.DataFrame({"page_content": embed_mat})
    df['vector'].to_csv(DATA_FOLDER + 'preprocessed_data/pretrained_spacy.csv', index=False)


if __name__ == '__main__':
    #print("start")
    #save()
    #print('go')\
    df = pd.DataFrame({'page_content': ['woda drzewa las']})
    x=recommend(df)

