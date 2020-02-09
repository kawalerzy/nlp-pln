import os
from datetime import datetime
from typing import List

from celery import Celery, group

from config import DATA_PATH
from scraping.pilkanoznapl.parser import extract_id_from_url
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
