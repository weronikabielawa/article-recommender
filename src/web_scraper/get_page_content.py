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

parser = 'html.parser'
links_df = pd.read_csv(DATA_FOLDER+'links/'+'spidersweb.csv')


for index, row in links_df.iterrows():
    resp = urllib.request.urlopen(row['spidersweb'])
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

    page_content = ''.join([div.get_text() for div in soup.findAll('p')])
    links_df.loc[index, 'page_content'] = page_content

    author = soup.findAll('div', attrs={'class': 'author__name'})[0].get_text()
    links_df.loc[index, 'author'] = author

    date = soup.findAll('div', attrs={'class': 'author__date'})[0].get_text()
    links_df.loc[index, 'date'] = date

    title = soup.findAll('title')[0].get_text()
    links_df.loc[index, 'title'] = title


links_df.to_csv(DATA_FOLDER+'raw_data/'+'spidersweb.csv')
#print(links_df.loc[0,'title'])