from datetime import datetime
from os.path import join

import pandas as pd
from bs4 import BeautifulSoup
from numpy import array_split
from pandas import Series
from sqlalchemy import bindparam, and_

from config import DATA_PATH, SQLALCHEMY_ENGINE_STR
from config.logger import logger
from db import get_engine_session, Article
from db.migrations.base_data_migration import BaseDataMigration
from scraping.pilkanoznapl.parser import parse_article


class AddHtmlAndFixText(BaseDataMigration):
    def start(self):
        self.load_fixed_articles()
        self.save_log()

    def assign_html(self, row: Series) -> str:
        return self.read_html(row['id'])

    def read_html(self, article_id: str) -> str:
        path = join(DATA_PATH, 'articles', f'{article_id}.html')
        with open(path, 'r') as file:
            html = file.read()
            soup = BeautifulSoup(html, 'lxml')
            content = soup.find_all('td', {'valign': 'top'})

            # Article content should be always in content[1]
            # if not, new case to investigate for parser
            try:
                if content is not None:
                    if len(content) <= 1:
                        logger.error(f'Irregular article: {article_id}. Content of length {len(content)}')
                        self.failed_entries.append(article_id)
                        if len(content) == 1:
                            return str(content[0])
                        return ""
                    else:
                        return str(content[1])
                else:
                    logger.error(f'Irregular article: {article_id}. Null content')
                    self.failed_entries.append(article_id)
                    return html
            except Exception:
                logger.exception(f"Unexpected exception while parsing article: {article_id}")
                return html

    def parse_text(self, row: Series) -> (str, str):
        text, source = parse_article(row['html'])

        if source is None:
            article_id = row['id']
            logger.error(f'Irregular article: {article_id}. Failed to extract source')
            self.failed_entries.append(article_id)

        return text, source

    def load_fixed_articles(self):
        merged_data = join(DATA_PATH, 'merged_data.csv')
        df = pd.read_csv(merged_data, sep='|')
        df = df.drop(['link', 'title', 'category', 'date'], axis=1)

        engine, session = get_engine_session(SQLALCHEMY_ENGINE_STR, verbose=False)
        articles = Article.__table__

        row_count = df.shape[0]
        updated_count = 0

        for frame in array_split(df, 140):
            """
            Split articles into chunks of size ~500
            and update values into database
            """
            chunk_size = frame.shape[0]
            logger.info(f'Inserting next chunk of size {chunk_size}')

            start = datetime.now()
            frame['html'] = frame.apply(self.assign_html, axis=1)
            frame[['text', 'source']] = frame.apply(self.parse_text, axis=1, result_type="expand")
            end = datetime.now()

            logger.info(f'Created chunk in: {end - start}')
            logger.info(f'Starting update')

            start = datetime.now()
            stmt = articles.update().where(
                and_(articles.c.id == bindparam('id'), articles.c.source is not None)).values({
                    'id': bindparam('id'),
                    'html': bindparam('html'),
                    'text': bindparam('text'),
                    'source': bindparam('source')
                })

            engine.execute(
                stmt,
                frame.to_dict(orient="records")
            )

            end = datetime.now()
            updated_count += chunk_size
            logger.info(f'Updated chunk in: {end - start}')
            logger.info(f'Processed {updated_count}/{row_count} articles.')


if __name__ == '__main__':
    with AddHtmlAndFixText() as migration:
        migration.start()
