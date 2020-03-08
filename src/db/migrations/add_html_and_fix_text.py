from os.path import join

import pandas as pd
from bs4 import BeautifulSoup
from pandas import Series
from sqlalchemy import bindparam

from config import DATA_PATH, SQLALCHEMY_ENGINE_STR
from db import get_engine_session, Article
from scraping.pilkanoznapl.parser import parse_article


def load_fixed_articles():
    merged_data = join(DATA_PATH, 'merged_data.csv')
    df = pd.read_csv(merged_data, sep='|')
    df = df.drop(['link', 'title', 'category', 'date'], axis=1)

    df['html'] = df.apply(assign_html, axis=1)
    df[['text', 'source']] = df.apply(parse_text, axis=1, result_type="expand")

    engine, session = get_engine_session(SQLALCHEMY_ENGINE_STR, verbose=False)
    articles = Article.__table__

    stmt = articles.update().where(articles.c.id == bindparam('id')).values({
        'id': bindparam('id'),
        'html': bindparam('html'),
        'text': bindparam('text'),
        'source': bindparam('source')
    })

    engine.execute(
        stmt,
        df.to_dict(orient="records")
    )


def assign_html(row: Series) -> str:
    return read_html(row['id'])


def read_html(article_id: str) -> str:
    path = join(DATA_PATH, 'articles', f'{article_id}.html')
    with open(path, 'r') as file:
        html = file.read()
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find_all('td', {'valign': 'top'})
        return str(content[1]) if content is not None else html


def parse_text(row: Series) -> (str, str):
    return parse_article(row['html'])


load_fixed_articles()
