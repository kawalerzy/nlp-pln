from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, create_session


def get_engine_session(conn_str: str, verbose=True) -> (Engine, scoped_session):
    """
    Creates and returns new thread-local sqlalchemy session
    :param conn_str: sqlalchemy database connection string
    :param verbose: if set to true, log all statements to default log handler
    :return: tuple with engine and session
    """
    engine: Engine = create_engine(conn_str, echo=verbose)
    session: scoped_session = scoped_session(lambda: create_session(bind=engine))
    return engine, session
