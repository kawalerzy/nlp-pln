from sqlalchemy import create_engine

from config import SQLALCHEMY_ENGINE_STR
from db import Base


def init_db():
    """
    Creates all tables for defined sqlalchemy models
    :return:
    """
    engine = create_engine(SQLALCHEMY_ENGINE_STR)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)