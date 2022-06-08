import os
import pandas as pd
import morfeusz2
import re
#from pystempel import Stemmer

DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')

df = pd.read_csv(DATA_FOLDER+'raw_data/ekologia.csv')


def cut_ending(df, end_str, col_name='page_content'):
    df[col_name] = df.apply(lambda row: row[col_name].split(end_str)[0], axis=1)
    return df


def remove_http(df, col_name='page_content'):
    df[col_name] = df.apply(lambda row: re.sub(r"http\S+", "", row[col_name]), axis=1)
    return df


def remove_puncuation(df, col_name='page_content'):
    punctuation = '.,();-„”-:–?!"&'
    df[col_name] = df.apply(lambda row: "".join([i for i in row[col_name] if i not in punctuation]),
                                        axis=1)
    return df


def remove_stopwords(df, col_name='page_content'):
    stop_words = open(DATA_FOLDER + 'helpers/polish_stopwords.txt').read().split("\n")
    df[col_name] = df.apply(lambda row: " ".join([i for i in row[col_name].split(" ") if i not in
                                                        stop_words]), axis=1)
    return df


def lowercase(df, col_name='page_content'):
    df[col_name] = df.apply(lambda row: " ".join([i.lower() for i in row[col_name].split(" ")]), axis=1)
    return df

def remove_tokens(df, col_name='page_content'):
    tokens = ['\r', '\n', '\xa0']
    for token in tokens:
        df[col_name] = df.apply(lambda row: row[col_name].replace(token, ""), axis=1)

    return df

#def stemming(df):
#    stemmer = StempelStemmer.polimorf()

#    df['page_content'] = df.apply(lambda row: " ".join([stemmer(i) for i in row['page_content'].split(" ")]), axis=1)
#    return df

#print(df['page_content'])
#print(remove_puncuation(df)['without_puncuation'])

#stop_words = open(DATA_FOLDER+'helpers/polish_stopwords.txt').read().split("\n")


def lemme(df, col_name='page_content'):

    def lem(s):
        result = []
        morf = morfeusz2.Morfeusz()
        a = morf.analyse(s)
        i=0
        for j in a:
            if j[0] == i:
                i += 1
                result.append(j[2][1].split(':')[0])
        return " ".join(result)


    for index, row in df.iterrows():
        df.loc[index, col_name] = lem(row[col_name])

    return df


def preprocess(df, col_name='page_content'):
    # to remove nan (there was 1 example found)
    df = df[~df[col_name].isna()]

    #for ekologia
    df = cut_ending(df, 'Ekologia.')
    #for interia
    df = cut_ending(df, 'Korzystanie z portalu oznacza akceptację Regulaminu.')
    # for zielonewiadomosci.pl
    df = cut_ending(df, 'Źródło')
    df = remove_http(df, col_name)
    df = remove_tokens(df, col_name)
    df = remove_puncuation(df, col_name)
    df = lowercase(df, col_name)
    df = remove_stopwords(df, col_name)
    #df = lemme(df, col_name)


    return df

