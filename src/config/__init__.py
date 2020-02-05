import os
from pathlib import Path

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = str(Path(CONFIG_DIR).parents[1])

DATA_PATH = '{}/data'.format(str(Path(CONFIG_DIR).parents[1]))
PAGES_PATH = '{}/pages'.format(str(Path(CONFIG_DIR).parents[1]))
