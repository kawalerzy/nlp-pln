import os
from datetime import datetime

import requests
from requests import Session

from config import PAGES_PATH, DATA_PATH
from scraping.pilkanoznapl import MAX_PAGE_NUM, categories, page_limits


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


def get_search_params(page_id: int, category_id: int) -> dict:
    return {
        "kategoria": str(category_id),
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
        "kategorie": str(category_id),
        "maxstrona": str(MAX_PAGE_NUM),
        "sortOrder": "desc",
        "sortColumn": "c.created"
    }


def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0'
    }


def save_next_page(page_id: int, category_id: int, session: Session):
    folder_name = categories[category_id]
    path = os.path.join(DATA_PATH, 'pilkanoznapl', folder_name, "{}.html".format(page_id))
    if os.path.exists(path):
        print('Page: {} already saved'.format(page_id))
        return

    headers = get_headers()
    search_params = get_search_params(page_id, category_id)
    url = 'https://pilkanozna.pl/index.php?option=com_wyszukiwarka_art&sekcja=20&kategoria={}&Itemid=9'.format(
        category_id)
    response = session.post(url, headers=headers, data=search_params)

    with open(path, 'w') as file:
        file.write(response.text)


def save_archive_range(from_range=0, category_id=64):
    session = requests.Session()
    category_name = categories[category_id]
    max_range = page_limits[category_id]

    for page_id in range(from_range, max_range):
        start = datetime.now()
        save_next_page(page_id, category_id, session)
        end = datetime.now()
        print('{}: Saved page {} in {}'.format(category_name, page_id, end - start))


def save_categories():
    for category_id in categories.keys():
        category_name = categories[category_id]
        category_data_dir = os.path.join(DATA_PATH, 'pilkanoznapl', category_name)

        if not os.path.exists(category_data_dir):
            os.mkdir(category_data_dir)

        print('Scrapping category: {}'.format(category_id))
        save_archive_range(1, category_id)


def save_article(url: str, path: str) -> None:
    response = requests.get(url)
    with open(path, 'w') as file:
        file.write(response.text)

