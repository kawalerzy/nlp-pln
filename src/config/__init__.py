import json
import operator
import os
from functools import reduce
from pathlib import Path

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = str(Path(CONFIG_DIR).parents[1])
DATA_PATH = '{}/data'.format(ROOT_PATH)
PAGES_PATH = '{}/pages'.format(ROOT_PATH)


class ConfigLoader:
    def __init__(self):
        self.auth_file = os.path.join(ROOT_PATH, 'auth.json')
        self.config = {}
        self.__load__()

    def get(self, path: str, default=""):
        try:
            return reduce(operator.getitem, path.split('.'), self.config)
        except KeyError:
            return default

    def __load__(self):
        with open(self.auth_file, 'r') as conf:
            self.config = json.loads(conf.read())


loader = ConfigLoader()

CELERY_BROKER_URL = loader.get('CELERY.BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

PSYCOPG2_CONN_STR = "host={} port={} dbname={} user={} password={}".format(
    loader.get('DB.HOST'),
    loader.get('DB.PORT'),
    loader.get('DB.NAME'),
    loader.get('DB.USER'),
    loader.get('DB.PASSWORD')
)

DEFAULT_SQLALCHEMY_ENGINE_STR = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    loader.get('DB.USER'),
    loader.get('DB.PASSWORD'),
    loader.get('DB.HOST'),
    loader.get('DB.PORT'),
    loader.get('DB.NAME')
)

SQLALCHEMY_ENGINE_STR = DEFAULT_SQLALCHEMY_ENGINE_STR

