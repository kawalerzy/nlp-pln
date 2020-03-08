import os
import time
from datetime import datetime
from os.path import join
from typing import List

import pandas as pd
from bs4 import BeautifulSoup
from celery import Celery, group
from pandas import Series
from sqlalchemy import bindparam

from config.dir import DATA_PATH
from db import Article, get_engine_session
from distributed import DBTask, SQLALCHEMY_ENGINE_STR
from scraping.pilkanoznapl import categories_map
from scraping.pilkanoznapl.parser import extract_id_from_url, parse_article_range, parse_article
from scraping.pilkanoznapl.scrapper import save_article

celery = Celery(__name__, autofinalize=False)


@celery.task(name='SCRAP_SINGLE_ARTICLE')
def scrap_single_article(url: str):
    article_id = extract_id_from_url(url)
    path = os.path.join(DATA_PATH, 'pilkanoznapl', 'articles', '{}.html'.format(article_id))
    if os.path.exists(path):
        print('Article {} already scrapped'.format(article_id))
        return
    try:
        start = datetime.now()
        save_article(url, path)
        end = datetime.now()
        print('Scrapped article: {} in {}'.format(url, end - start))
    except Exception as ex:
        print('Failed to scrap article: {}'.format(url))
        print(ex)
    return


@celery.task(name='SCRAP_ARTICLES')
def scrap_articles(links: List[str]):
    group(scrap_single_article.s(url) for url in links)()
    return


@celery.task(name='PARSE_ARTICLE_CHUNK')
def parse_articles_range(article_paths: List[str], file_name: str):
    print('Received parsing task: {}'.format(file_name))
    out_path = os.path.join(DATA_PATH, file_name + '.csv')
    articles_df = parse_article_range(article_paths)
    articles_df.to_csv(out_path, sep='|', index=False)

    return


@celery.task(base=DBTask, bind=True)
def merge_meta_and_articles(self):
    paths = [os.path.join(DATA_PATH, 'parsed', f'parsed_{df_id}.csv') for df_id in range(0, 12)]
    article_meta_data = pd.read_csv(os.path.join(DATA_PATH, 'merged_data.csv'), sep='|')
    article_data = pd.concat([pd.read_csv(f, sep='|') for f in paths])
    merged = article_meta_data.merge(article_data, on='id')
    merged = merged.rename(
        columns={
            'links_list': 'external_links',
            'raw_text': 'text'
        }
    )
    merged.category = merged.category.map(categories_map)
    self.engine.execute(
        Article.__table__.insert(),
        merged.to_dict(orient="records")
    )


@celery.task(base=DBTask, bind=True)
def load_articles(self):
    merged_data = os.path.join(DATA_PATH, 'merged_data.csv')
    df = pd.read_csv(merged_data, sep='|')
    df.category = df.category.map(categories_map)
    t0 = time.time()
    self.engine.execute(
        Article.__table__.insert(),
        df.to_dict(orient="records")
    )
    print(f'Inserted {len(df)} in: {time.time() - t0}')
