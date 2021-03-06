import os
import pandas as pd
import morfeusz2
import re
#from pystempel import Stemmer

DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')


def cut_ending(df, end_str, col_name='page_content'):
    df[col_name] = df.apply(lambda row: row[col_name].split(end_str)[0], axis=1)
    return df


def remove_http(df, col_name='page_content'):
    df[col_name] = df.apply(lambda row: re.sub(r"http\S+", "", row[col_name]), axis=1)
    return df


def remove_puncuation(df, col_name='page_content'):
    punctuation = '.,();-„”-:–?!"&/'
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
    morf = morfeusz2.Morfeusz()
    def lem(s):
        result = []
        a = morf.analyse(s)
        i=0
        for j in a:
            if j[0] == i:
                i += 1
                result.append(j[2][1].split(':')[0])
        return " ".join(result)

    #for index, row in df.iterrows():
        #df.loc[index, col_name] = lem(row[col_name])
    df[col_name] = df.apply(lambda row: lem(row[col_name]), axis=1)

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
    df = lemme(df, col_name)

    return df


def chunkify(df: pd.DataFrame, chunk_size: int):
    start = 0
    length = df.shape[0]

    # If DF is smaller than the chunk, return the DF
    if length <= chunk_size:
        yield df[:]
        return

    # Yield individual chunks
    while start + chunk_size <= length:
        yield df[start:chunk_size + start]
        start = start + chunk_size

    # Yield the remainder chunk, if needed
    if start < length:
        yield df[start:]




if __name__ == '__main__':
    df_list = [
        'ekologia.csv',
        'interia.csv',
        'spidersweb.csv',
        'zielonewiadomosci.csv',
        'ziemianarozdrozu.csv'
    ]
    dfs = []
    for df_name in df_list:
        for chunk in pd.read_csv(DATA_FOLDER + 'raw_data/' + df_name, chunksize=20):
            x = preprocess(chunk)
            dfs.append(x)

        print(df_name)

    dfs = pd.concat(dfs, ignore_index=True)
    dfs[['page_content','url']].to_csv(DATA_FOLDER + 'preprocessed_data/preprocessed_data.csv', index=False)
    dfs['url'].to_csv(DATA_FOLDER + 'preprocessed_data/url.csv', index=False)