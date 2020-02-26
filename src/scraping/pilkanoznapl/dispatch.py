import os

import numpy as np
import pandas as pd

from config import DATA_PATH
from distributed.celery_setup import celery_entrypoint
from scraping.pilkanoznapl.tasks import scrap_articles, parse_articles_range, merge_meta_and_articles
from util.split import split


def dispatch_scrapping_tasks():
    path = os.path.join(DATA_PATH, 'pilkanoznapl', 'merged_data.csv')
    merged_df = pd.read_csv(path, sep='|')
    for g, df in merged_df.groupby(np.arange(len(merged_df)) // 100):
        links = df['link'].tolist()
        date = df['date'].tolist()
        scrap_articles.delay(links)
        print('Dispatched tasks for scraping: {} to {}'.format(date[0], date[-1]))


def dispatch_parsing_tasks():
    path = os.path.join(DATA_PATH, 'articles')
    threads_num = 12
    article_paths = list(map(lambda x: os.path.join(path, x), os.listdir(path)))
    article_chunks = list(split(article_paths, threads_num))
    for num, chunk in enumerate(article_chunks):
        print('Dispatching tasks {} ...'.format(num))
        parse_articles_range.delay(chunk, 'parsed_{}'.format(num))


def dispatch_load():
    merge_meta_and_articles.delay()


celery = celery_entrypoint()
dispatch_load()
