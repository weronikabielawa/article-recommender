import pytest
import pandas as pd

from src.preprocessing.preprocessing import remove_puncuation, remove_stopwords, lowercase

# todo: 1. add test for lemmatization, 2. add more complex fixtures


@pytest.fixture
def df_with_puncuation():
    return pd.DataFrame({'text': ['przykładowy, tekst ze znakami.']})


@pytest.fixture
def df_without_puncuation():
    return pd.DataFrame({'text': ['przykładowy tekst ze znakami']})


@pytest.fixture
def df_with_stopwords():
    return pd.DataFrame({'text': ['ale mi to się podoba']})


@pytest.fixture
def df_without_stopwords():
    return pd.DataFrame({'text': ['podoba']})


@pytest.fixture
def df_uppercase():
    return pd.DataFrame({'text': ['Przykład Numer Jeden']})


@pytest.fixture
def df_lowercase():
    return pd.DataFrame({'text': ['przykład numer jeden']})


def test_remove_puncuation(df_with_puncuation, df_without_puncuation):
    assert df_without_puncuation['text'].loc[0] == remove_puncuation(df_with_puncuation, 'text')['text'].loc[0]


def test_remove_stopwords(df_with_stopwords, df_without_stopwords):
    assert df_without_stopwords['text'].loc[0] == remove_stopwords(df_with_stopwords, 'text')['text'].loc[0]


def test_lowercase(df_uppercase, df_lowercase):
    assert df_lowercase['text'].loc[0] == lowercase(df_uppercase, 'text')['text'].loc[0]