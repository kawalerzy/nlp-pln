import os
from pathlib import Path

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = str(Path(CONFIG_DIR).parents[1])
DATA_PATH = '{}/data'.format(ROOT_PATH)
PAGES_PATH = '{}/pages'.format(ROOT_PATH)
