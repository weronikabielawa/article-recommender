from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
import pandas as pd

from src.preprocessing.preprocessing import preprocess


def recommend_doc2vec(article):
    DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')
    df = pd.read_csv(DATA_FOLDER+'preprocessed_data/preprocessed_data.csv')

    df['page_content'] = df['page_content'].str.split(" ")
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(df['page_content'])]

    model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)

    # preprocessing input
    article_df = preprocess(pd.DataFrame({'page_content': [article]}))
    article_preprocessed = article_df.loc[0, 'page_content'].split(" ")

    vector = model.infer_vector(article_preprocessed)
    index = model.dv.most_similar(vector)[0][0]

    return df.loc[index, 'url']
