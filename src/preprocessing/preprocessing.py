import os
import pandas as pd
import morfeusz2
#from pystempel import Stemmer

DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')

df = pd.read_csv(DATA_FOLDER+'raw_data/ekologia.csv')


def remove_puncuation(df, col_name):
    punctuation = ['.', ',']
    df[col_name] = df.apply(lambda row: "".join([i for i in row[col_name] if i not in punctuation]),
                                        axis=1)
    return df


def remove_stopwords(df, col_name):
    stop_words = open(DATA_FOLDER + 'helpers/polish_stopwords.txt').read().split("\n")
    df[col_name] = df.apply(lambda row: " ".join([i for i in row[col_name].split(" ") if i not in
                                                        stop_words]), axis=1)
    return df


def lowercase(df, col_name):
    df[col_name] = df.apply(lambda row: " ".join([i.lower() for i in row[col_name].split(" ")]), axis=1)
    return df

#def stemming(df):
#    stemmer = StempelStemmer.polimorf()

#    df['page_content'] = df.apply(lambda row: " ".join([stemmer(i) for i in row['page_content'].split(" ")]), axis=1)
#    return df

#print(df['page_content'])
#print(remove_puncuation(df)['without_puncuation'])

#stop_words = open(DATA_FOLDER+'helpers/polish_stopwords.txt').read().split("\n")

def lemme(df, col_name):

    def lem(s):
        result = []
        morf = morfeusz2.Morfeusz()
        a = morf.analyse(s)
        i=0
        for j in a:
            if j[0] == i:
                i += 1
                result.append(j[2][1])
        return "".join(s)
    #morf = morfeusz2.Morfeusz()

    df[col_name] = df.apply(lambda row: lem(row[col_name]), axis=1)
    return df

df = df.head(5)
#print(x)
df = remove_puncuation(df, 'page_content')
df = lowercase(df, 'page_content')
df = remove_stopwords(df, 'page_content')
print(df['page_content'])
df = lemme(df, 'page_content')
print(df['page_content'].loc[0])
#print(df)