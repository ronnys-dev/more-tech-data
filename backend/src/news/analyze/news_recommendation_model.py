import pickle

import numpy as np
import pandas as pd
from natasha import MorphVocab, NamesExtractor
from nltk import regexp_tokenize
from pymorphy2 import MorphAnalyzer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

with open('/backend/src/news/analyze/dct_word_final.pickle', 'rb') as f:
    dct_words = pickle.load(f)

names_extractor = NamesExtractor(MorphVocab())
morph = MorphAnalyzer()


def read_from_file(file):
    """
    Function to read from file
    """
    f = open(file, 'r', encoding='utf-8')
    lst = []
    while True:
        s = f.readline().strip('\n"')
        if not s:
            break
        lst.append(s)
    return pd.DataFrame(lst, columns=["text"])


def pos(word):
    return morph.parse(word)[0].tag.POS


def delete(row: str) -> str:
    functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO'}  # function words
    return " ".join([word.lower() for word in row.split() if pos(word) not in functors_pos])


def tokenize_n_normalize(sent, pat=r"(?u)\b\w\w+\b"):
    return [morph.parse(tok)[0].normal_form for tok in regexp_tokenize(sent, pat)]


def have_name(row: str) -> bool:
    matches = names_extractor(row)
    for i in matches:
        if i.fact.first is None or i.fact.last is None:
            return False
    return True


class NewsPreprocessor(StandardScaler):
    """
    Preprocessor, making matrix of matches from list of news texts
    """

    def __init__(self, min_word_amount: int = 100, min_difference: float = 0.5):
        super().__init__()
        self.min_word_amount = min_word_amount
        self.min_difference = min_difference

    def fit(self, X: pd.Series, y: pd.Series):
        return self

    def transform(self, X: pd.Series, y: pd.Series = None) -> pd.DataFrame:

        flag_for_percent = X.apply(lambda x: "%" in x)
        X = X.apply(delete).map(lambda x: " ".join(tokenize_n_normalize(x)))
        flag_for_name = X.apply(have_name)

        preprocess_dict = {
            key: val
            for key, val in dct_words.items()
            if val[0] > self.min_word_amount and abs(val[1] - val[2]) > self.min_difference
        }
        res_df = pd.DataFrame(columns=preprocess_dict.keys(), index=X.index)
        res_df["text"] = np.array(X)
        for key in preprocess_dict.keys():
            res_df[key] = X.apply(lambda x: key in x)
        res_df["names"] = flag_for_name
        res_df["percent"] = flag_for_percent
        res_df = res_df.drop(columns='text')
        return res_df

    def fit_transform(self, X: pd.Series, y: pd.Series = None) -> pd.DataFrame:
        self.fit(X, y)
        return self.transform(X, y)


class NewsModel(LinearRegression):
    """
    Regression that gives numeric priority for news
    """

    def __init__(self, method='linear'):
        super().__init__()
        self.method = method
        self.W = None

    def fit(self, X: pd.DataFrame, y: pd.Series):
        if 'text' in X.columns:
            X = X.drop(columns='text')
        args = [dct_words[key] for key in X.columns]
        self.W = np.array([(w[1] - w[2]) * w[0] for w in args])
        return self

    def predict(self, X: pd.DataFrame) -> pd.Series:
        if 'text' in X.columns:
            X = X.drop(columns='text')
        return X.apply(lambda x: (x * self.W).mean(), axis=1)

    def fit_predict(self, X: pd.DataFrame, y: pd.Series) -> pd.Series:
        self.fit(X, y)
        return self.predict(X)

    def score(self, X=pd.DataFrame, y: pd.Series = None) -> float:
        return super().score(X, y)


def get_recommendations(df, role: str) -> dict[str, list[str]]:
    df = pd.Series(dict(df))
    news_pipe = Pipeline(
        steps=[
            ('prep', NewsPreprocessor(min_word_amount=200, min_difference=0.4)),
            ('model', NewsModel()),
        ]
    )
    scores = list(news_pipe.fit_predict(df).sort_values().index)
    if role == 'accountant':
        return scores[:3]
    elif role == 'director':
        return scores[-1:-4:-1]
    return None
