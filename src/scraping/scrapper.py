import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import PAGES_PATH


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


def parse_table(html: str):
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.find('table', {'class': 'adminlist'}).find_all("tr")

    columns = ['link', 'title', 'category', 'date']
    df = pd.DataFrame(columns=columns)
    for row in rows:
        cells = row.find_all("td")

        count = 0
        entry_dict = {}
        for cell in cells:
            link = cell.find('a')
            if link is not None:
                href = link['href']
                if href != 'javascript:kat(64)':
                    entry_dict[columns[count]] = base_url + href
                    count += 1

            entry_dict[columns[count]] = cell.get_text().strip()
            count += 1

        if entry_dict:
            print(entry_dict)
            df = df.append(entry_dict, ignore_index=True)

    print(df)


# create_test_html()

html_path = os.path.join(PAGES_PATH, 'pilkanoznapl', 'table.html')
base_url = 'https://pilkanozna.pl'
table_html = ''
with open(html_path) as f:
    table_html = f.read()

parse_table(table_html)
