import os

import pandas as pd
import numpy as np

from config import DATA_PATH
from distributed.celery_setup import celery_entrypoint
from scraping.pilkanoznapl.tasks import scrap_articles


def dispatch_scrapping_tasks():
    path = os.path.join(DATA_PATH, 'pilkanoznapl', 'merged_data.csv')
    merged_df = pd.read_csv(path, sep='|')
    for g, df in merged_df.groupby(np.arange(len(merged_df)) // 100):
        links = df['link'].tolist()
        date = df['date'].tolist()
        scrap_articles.delay(links)
        print('Dispatched tasks for scraping: {} to {}'.format(date[0], date[-1]))


celery = celery_entrypoint()
dispatch_scrapping_tasks()
