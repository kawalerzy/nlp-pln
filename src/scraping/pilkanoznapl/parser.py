import os
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

from config import DATA_PATH
from scraping.pilkanoznapl import columns, base_url


def parse_table(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.find('table', {'class': 'adminlist'}).find_all("tr")

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
            df = df.append(entry_dict, ignore_index=True)

    return df


def parse_archive() -> None:
    out_path = os.path.join(DATA_PATH, 'pilkanoznapl', 'table_data.csv')
    in_dir = os.path.join(DATA_PATH, 'pilkanoznapl', 'raw')

    df = pd.DataFrame(columns=columns)
    for file in sorted(os.listdir(in_dir)):
        try:
            start = datetime.now()
            path = os.path.join(in_dir, file)
            with open(path, 'r') as page:
                text = page.read()
                df = df.append(parse_table(text))
            end = datetime.now()
            print('Parsed file {} in {}'.format(file, end - start))
        except Exception as err:
            print("Unexpected error while parsing file: {}".format(file))
            print(err)

    df.to_csv(out_path, index=True)


def prepare_table() -> None:
    in_path = os.path.join(DATA_PATH, 'pilkanoznapl', 'table_data.csv')
    out_path = os.path.join(DATA_PATH, 'pilkanoznapl', 'sorted_table_data.csv')
    df = pd.read_csv(in_path)
    df = df.drop(columns='index')
    df = df.sort_values('date')
    df.to_csv(out_path, index=False, header=True)
