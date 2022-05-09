import os
import pandas as pd
#from pystempel import Stemmer

DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')

df = pd.read_csv(DATA_FOLDER+'raw_data/ekologia.csv')


def remove_puncuation(df):
    punctuation = ['.', ',']
    df['page_content'] = df.apply(lambda row: "".join([i for i in row['page_content'] if i not in punctuation]),
                                        axis=1)
    return df


def remove_stopwords(df):
    stop_words = open(DATA_FOLDER + 'helpers/polish_stopwords.txt').read().split("\n")
    df['page_content'] = df.apply(lambda row: " ".join([i for i in row['page_content'].split(" ") if i not in
                                                        stop_words]), axis=1)
    return df


def lowercase(df):
    df['page_content'] = df.apply(lambda row: " ".join([i.lower() for i in row['page_content'].split(" ")]), axis=1)
    return df

#def stemming(df):
#    stemmer = StempelStemmer.polimorf()

#    df['page_content'] = df.apply(lambda row: " ".join([stemmer(i) for i in row['page_content'].split(" ")]), axis=1)
#    return df

#print(df['page_content'])
#print(remove_puncuation(df)['without_puncuation'])

#stop_words = open(DATA_FOLDER+'helpers/polish_stopwords.txt').read().split("\n")

df = remove_puncuation(df)
df = lowercase(df)
df = remove_stopwords(df)
#df = stemming(df)
print(df['page_content'])
#print(df)