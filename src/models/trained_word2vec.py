from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
import pandas as pd

from src.preprocessing.preprocessing import preprocess
global DATA_FOLDER
DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')

def recommend_doc2vec(article_preprocessed):
    model = Doc2Vec.load(DATA_FOLDER+'preprocessed_data/trained_model')
    article_preprocessed = article_preprocessed.loc[0, 'page_content'].split(" ")
    vector = model.infer_vector(article_preprocessed)
    index = model.dv.most_similar(vector)[0][0]

    return pd.read_csv(DATA_FOLDER+'preprocessed_data/url.csv').loc[index, 'url']


def train():
    DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')
    df = pd.read_csv(DATA_FOLDER+'preprocessed_data/preprocessed_data.csv')
    df = df[~df['page_content'].isna()]
    df['page_content'] = df['page_content'].str.split(" ")
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(df['page_content'])]
    model = Doc2Vec(documents, vector_size=10, window=2, min_count=1, workers=4)
    model.save(DATA_FOLDER+'preprocessed_data/trained_model')


if __name__=='__main__':
    train()