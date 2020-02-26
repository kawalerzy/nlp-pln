from abc import ABC

from celery import Task
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session

from config import SQLALCHEMY_ENGINE_STR
from db.session import get_engine_session


class DBTask(Task, ABC):
    """
    Base class for database tasks with separate SQLAlchemy session
    """
    _session: scoped_session = None
    _engine: Engine = None

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self._session is not None:
            self._session.remove()

    @property
    def session(self) -> scoped_session:
        if self._session is None:
            _, self._session = get_engine_session(SQLALCHEMY_ENGINE_STR, verbose=False)
        return self._session

    @property
    def engine(self) -> scoped_session:
        if self._engine is None:
            self._engine, _ = get_engine_session(SQLALCHEMY_ENGINE_STR, verbose=False)
        return self._engine
