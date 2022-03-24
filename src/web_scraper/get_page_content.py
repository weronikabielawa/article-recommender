from typing import List
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import pandas as pd
import os
from collections import namedtuple
import re
global DATA_FOLDER
DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')

# todo: REFACTOR!
parser = 'html.parser'
"""links_df = pd.read_csv(DATA_FOLDER+'links/'+'spidersweb.csv')


for index, row in links_df.iterrows():
    resp = urllib.request.urlopen(row['url'])
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

    page_content = ''.join([div.get_text() for div in soup.findAll('p')])
    links_df.loc[index, 'page_content'] = page_content

    author = soup.findAll('div', attrs={'class': 'author__name'})[0].get_text()
    links_df.loc[index, 'author'] = author

    date = soup.findAll('div', attrs={'class': 'author__date'})[0].get_text()
    links_df.loc[index, 'date'] = date

    title = soup.findAll('title')[0].get_text()
    links_df.loc[index, 'title'] = title


links_df.to_csv(DATA_FOLDER+'raw_data/'+'spidersweb.csv', index=False)"""

# interia
"""links_df = pd.read_csv(DATA_FOLDER+'links/'+'interia.csv')


for index, row in links_df.iterrows():
    resp = urllib.request.urlopen(row['url'])
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

    try:
        page_content = ''.join([div.get_text() for div in soup.findAll('p', attrs={'class':None})])
        links_df.loc[index, 'page_content'] = page_content
        print(page_content)

        author = soup.findAll('span', attrs={'itemprop': 'name'})# [0].get_text()
        links_df.loc[index, 'author'] = author
        print(author)

        date = soup.findAll('meta', attrs={'itemprop': 'datePublished'})[0].get("content")
        links_df.loc[index, 'date'] = date
        print(date)

        title = soup.findAll('div', attrs={'class': 'article-header-body'})[0].get_text()
        links_df.loc[index, 'title'] = title
        print(title)
    except:
        pass

    #break

#print(links_df)

links_df.to_csv(DATA_FOLDER+'raw_data/'+'interia.csv', index=False)"""

# zielone wiadomosci
"""links_df = pd.read_csv(DATA_FOLDER+'links/'+'zielonewiadomosci.csv')


for index, row in links_df.iterrows():
    resp = urllib.request.urlopen(row['url'])
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

    try:
        page_content = ''.join([div.get_text() for div in soup.findAll('p')])
        links_df.loc[index, 'page_content'] = page_content
        print(page_content)

        author = ' ; '.join(i.get_text() for i in soup.findAll('a', attrs={'class': 'autor-single2'}))
        links_df.loc[index, 'author'] = author
        print(author)

        date = soup.findAll('div', attrs={'class': 'autor-single-date'})[0].get_text()
        links_df.loc[index, 'date'] = date
        print(date)

        title = soup.findAll('title')[0].get_text()
        links_df.loc[index, 'title'] = title
        print(title)
    except:
        pass



#print(links_df)

links_df.to_csv(DATA_FOLDER+'raw_data/'+'zielonewiadomosci.csv', index=False)"""


"""
links_df = pd.read_csv(DATA_FOLDER+'links/'+'ziemianarozdrozu.csv')

i = 0
for index, row in links_df.iterrows():
    print(1)
    i+=1

    try:
        resp = urllib.request.urlopen(row['url'])
        soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
        page_content = ''.join([div.get_text() for div in soup.findAll('p')])
        links_df.loc[index, 'page_content'] = page_content
        #print(page_content)

        #author = ' ; '.join(i.get_text() for i in soup.findAll('a', attrs={'class': 'autor-single2'}))
        #links_df.loc[index, 'author'] = author
        #print(author)

        #date = soup.findAll('div', attrs={'class': 'autor-single-date'})[0].get_text()
        #links_df.loc[index, 'date'] = date
        #print(date)

        title = soup.findAll('title')[0].get_text()
        links_df.loc[index, 'title'] = title
        print(title)
    except:
        pass




#print(links_df)

links_df.to_csv(DATA_FOLDER+'raw_data/'+'ziemianarozdrozu.csv', index=False)"""



links_df = pd.read_csv(DATA_FOLDER+'links/'+'ekologia.csv')

i = 0
for index, row in links_df.iterrows():
    print(1)
    i+=1

    try:
        resp = urllib.request.urlopen(row['url'])
        soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
        page_content = ''.join([div.get_text() for div in soup.findAll('article', attrs={'itemprop':'articleBody'})])
        links_df.loc[index, 'page_content'] = page_content
        print(page_content)

        author = soup.findAll('meta', attrs={'name': 'author'})[0].get('content')
        links_df.loc[index, 'author'] = author
        print(author)

        date = soup.findAll('meta', attrs={'name': 'article:published_time'})[0].get('content')
        links_df.loc[index, 'date'] = date
        print(date)

        title = soup.findAll('title')[0].get_text()
        links_df.loc[index, 'title'] = title
        print(title)
    except:
        pass


#print(links_df)

links_df.to_csv(DATA_FOLDER+'raw_data/'+'ekologia.csv', index=False)




