import json
import operator
import os
from functools import reduce

from config.dir import ROOT_PATH


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
