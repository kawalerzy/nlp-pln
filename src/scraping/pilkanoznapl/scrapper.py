import os
from datetime import datetime

import requests
from requests import Session

from config import PAGES_PATH, DATA_PATH
from scraping.pilkanoznapl import MAX_PAGE_NUM


def create_test_html() -> None:
    table_url = 'https://pilkanozna.pl/index.php?option=com_wyszukiwarka_art&sekcja=20&kategoria=64&Itemid=9'
    table_response = requests.get(table_url)
    table_filepath = os.path.join(PAGES_PATH, 'pilkanoznapl', 'table.html')
    with open(table_filepath, 'w') as file:
        file.write(table_response.text)

    article_url = 'https://pilkanozna.pl/index.php/Wydarzenia/Ekstraklasa/1008557-antonio-dominguez-wzmocni-odzki-klub-sportowy.html'
    article_response = requests.get(article_url)
    article_filepath = os.path.join(PAGES_PATH, 'pilkanoznapl', 'article.html')
    with open(article_filepath, 'w') as file:
        file.write(article_response.text)


def get_search_params(page_id: int) -> dict:
    return {
        "kategoria": "64",
        "od": "7",
        "option": "com_wyszukiwarka_art",
        "task": "",
        "layout": "default",
        "boxchecked": "0",
        "controller": "wyszukiwarka",
        "view": "wyszukiwarka",
        "kanal": "",
        "sekcja": "20",
        "strona": str(page_id),
        "kategorie": "64",
        "maxstrona": str(MAX_PAGE_NUM),
        "sortOrder": "desc",
        "sortColumn": "c.created"
    }


def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0'
    }


def save_next_page(page_id: int, session: Session):
    path = os.path.join(DATA_PATH, 'pilkanoznapl', 'raw', "{}.html".format(page_id))
    if os.path.exists(path):
        print('Page: {} already saved'.format(page_id))
        return

    headers = get_headers()
    search_params = get_search_params(page_id)
    url = 'https://pilkanozna.pl/index.php?option=com_wyszukiwarka_art&sekcja=20&kategoria=64&Itemid=9'
    response = session.post(url, headers=headers, data=search_params)

    with open(path, 'w') as file:
        file.write(response.text)


def save_archive_range(from_range=0, to_range=MAX_PAGE_NUM):
    session = requests.Session()
    for page_id in range(from_range, to_range):
        start = datetime.now()
        save_next_page(page_id, session)
        end = datetime.now()
        print('Saved page: {} in {}'.format(page_id, end - start))
