import os

from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session

from config import SQLALCHEMY_ENGINE_STR, ROOT_PATH
from db import get_engine_session


class BaseDataMigration:
    session: scoped_session
    engine: Engine
    failed_entries: []
    log: str

    def __enter__(self):
        return self

    def start(self):
        pass

    def __init__(self, log=os.path.join(ROOT_PATH, 'migration_errors.log')):
        self.engine, self.session = get_engine_session(SQLALCHEMY_ENGINE_STR, verbose=False)
        self.log = log
        self.failed_entries = []
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.remove()
        self.engine.dispose()
        self.save_log()

    def save_log(self):
        with open(self.log, 'a') as migration_log:
            migration_log.write('\n'.join(self.failed_entries))
