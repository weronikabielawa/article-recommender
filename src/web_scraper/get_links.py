from typing import List
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import pandas as pd
import os
from collections import namedtuple
import re


# main folder for for saving data
global DATA_FOLDER
DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../' + 'data/')

UrlSchema = namedtuple('UrlSchema', 'page_name page_addres attributes_to_filter filter fill')


def get_all_links(page: UrlSchema) -> List[str]:
    """function that for given address goes into pages and gets links """
    links = []
    page_number = 2
    while True:
        page_address = page.page_addres.replace("%", f"{page_number}")
        size = len(links)
        try:
            links = get_all_links_from_single_page(page_address, page.attributes_to_filter, links)
        except HTTPError:
            break

        if len(links) == size:
            break

        page_number += 1

    return links


def get_all_links_from_single_page(url: str, class_: str = None, list_of_links: List[str] = None) -> List[str]:
    """ function that returns links to articles that are on given site

    Args:
        url(str): link to site
        class_(str): attribute to filter (optional)
        list_of_links: list of links gathered so far (optional)

    Returns:
        list_of_links(List[str]): list of links
    """

    parser = 'html.parser'
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

    page_source = soup.findAll('div', attrs={'class': class_})
    for div in page_source:
        for link in div.find_all('a', href=True):
            if link['href'] not in list_of_links:
                list_of_links.append(link['href'])

    return list_of_links


def save_data_to_csv(folder: str, page_name: str, data: List[str]) -> None:
    """ function that converts list into pandas dataframe and saves it into csv"""

    dir_path = DATA_FOLDER + folder
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    df = pd.DataFrame(data=data, columns=['url'])
    df.to_csv((dir_path+'/'+page_name+'.csv'), index=False)


def filter_using_regex(pattern, list):
    """filter out some addresses"""
    return [url for url in list if re.match(pattern, url)]


def fill_page_link(link, list):
    """add beginning of the address"""
    return [link+url for url in list if link not in url]


"""if __name__ == '__main__':

    pages = [UrlSchema("interia", "https://zielona.interia.pl/klimat,nPack,%", 'tile-magazine', '.+nId.+', 'https://zielona.interia.pl'),
             UrlSchema("ekologia", "https://www.ekologia.pl/wiadomosci/srodowisko,s%/", 'kategoriaDivArtykul', None, None),
             UrlSchema("spidersweb", "https://spidersweb.pl/bizblog/category/srodowisko/page/%/", 'm-post__title', None, None),
             UrlSchema("ziemianarozdrozu", "https://ziemianarozdrozu.pl/artykuly?p=%", 'post cf', '/artykul/.+', 'https://ziemianarozdrozu.pl'),
             UrlSchema("zielonewiadomosci", "https://zielonewiadomosci.pl/tematy/ekologia/page/%/", 'featured-image', None, None)]

    for page in pages:
        links = get_all_links(page)
        #save_data_to_csv('links_unfiltered', page.page_name, links)

        if page.filter:
            links = filter_using_regex(page.filter, links)
            #save_data_to_csv('links_filtered', page.page_name, links)

        if page.fill:
            links = fill_page_link(page.fill, links)
            #save_data_to_csv('links_filled', page.page_name, links)

        save_data_to_csv('links', page.page_name, links)
"""
