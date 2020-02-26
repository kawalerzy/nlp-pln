from config import loader

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
SQLALCHEMY_ENGINE_STR = loader.get("DB.LOCAL_CONN_STR", DEFAULT_SQLALCHEMY_ENGINE_STR)
