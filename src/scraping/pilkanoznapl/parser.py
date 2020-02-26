import os
import re
from datetime import datetime
from typing import List
from urllib.parse import urlparse

import pandas as pd
from bs4 import BeautifulSoup
from pandas import Series

from config import DATA_PATH
from scraping.pilkanoznapl import columns, base_url, categories, months


def parse_article_range(article_paths: List[str]) -> pd.DataFrame:
    parsed_columns = ['id', 'raw_text', 'links_list']
    df = pd.DataFrame(columns=parsed_columns)

    for num, path in enumerate(article_paths):
        entry = {'id': os.path.basename(path).split('.')[0]}
        if num % 100 == 0:
            print('Parsed: {}/{}'.format(num, len(article_paths)))
        with open(path, 'r') as article:
            html = article.read()
            parsed_article_dict = parse_article(html)
            entry.update(parsed_article_dict)
            df = df.append(entry, ignore_index=True)

    return df


def parse_article(html: str) -> dict:
    soup = BeautifulSoup(html, 'lxml')
    try:
        content = soup.find_all('td', {'valign': 'top'})
        date = parse_date(content[0].text)
        article_content = content[1]
        raw_text = '.'.join(article_content.find_all(text=True))
        raw_links_list = soup.findAll('a', attrs={'href': re.compile("^http://")})
        links_list = [link.get('href') for link in raw_links_list if
                      urlparse(link.get('href')).netloc not in ['pilkanozna.pl', 'www.alexlopezit.com']]
        article_content_dict = {'date': date, 'raw_text': raw_text, 'links_list': links_list}
        return article_content_dict
    except Exception as ex:
        print(ex, html)
        return {}


def parse_table(html: str, category_id: int) -> pd.DataFrame:
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
                if href != 'javascript:kat({})'.format(category_id):
                    entry_dict[columns[count]] = base_url + href
                    count += 1

            entry_dict[columns[count]] = cell.get_text().strip()
            count += 1

        if entry_dict:
            df = df.append(entry_dict, ignore_index=True)

    return df


def parse_category(category_id: int) -> None:
    category_name = categories[category_id]
    out_path = os.path.join(DATA_PATH, 'pilkanoznapl', '{}_data.csv'.format(category_name))
    in_dir = os.path.join(DATA_PATH, 'pilkanoznapl', category_name)

    if os.path.exists(out_path):
        print('Category {} seems to be already parsed'.format(category_name))
        return

    df = pd.DataFrame(columns=columns)
    for file in os.listdir(in_dir):
        try:
            start = datetime.now()
            path = os.path.join(in_dir, file)
            with open(path, 'r') as page:
                text = page.read()
                df = df.append(parse_table(text, category_id))
            end = datetime.now()
            print('Parsed file {} in {}'.format(file, end - start))
        except Exception as err:
            print("Unexpected error while parsing file: {}".format(file))
            print(err)

    df = df.sort_values('date')
    df.to_csv(out_path, sep='|', index=False)


def parse_categories() -> None:
    for category_id in categories.keys():
        category_name = categories[category_id]
        print('Parsing category: {}'.format(category_name))
        parse_category(category_id)


def merge_categories() -> None:
    out_path = os.path.join(DATA_PATH, 'pilkanoznapl', 'merged_data.csv')
    paths = [os.path.join(DATA_PATH, 'pilkanoznapl', '{}_data.csv'.format(name)) for name in categories.values()]
    combined_df = pd.concat([pd.read_csv(f, sep='|') for f in paths])
    combined_df = combined_df.sort_values('date')
    combined_df.to_csv(out_path, sep='|', index=False)


def extract_id_from_url(url: str) -> str:
    article_str = url.split('/')[-1]
    article_id = article_str.split('-')[0]
    return article_id


def assign_id(row: Series) -> str:
    return extract_id_from_url(row['link'])


def assign_id_to_articles(df: pd.DataFrame) -> pd.DataFrame:
    df['id'] = df.apply(assign_id, axis=1)
    return df


def format_data():
    pth = os.path.join(DATA_PATH, 'merged_data.csv')
    df = pd.read_csv(pth, sep='|')
    df = assign_id_to_articles(df)
    df.to_csv(pth, sep='|', index=False)


def parse_date(date_string: str) -> datetime:
    date_string = re.compile(r'[\n\t]').sub("", date_string)
    date = date_string.split(' ')
    time = date[4].split(':')
    return datetime(int(date[3]), months[date[2]], int(date[1]), int(time[0]), int(time[1]))
