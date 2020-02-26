import psycopg2

from config import PSYCOPG2_CONN_STR

conn = psycopg2.connect(PSYCOPG2_CONN_STR)
cursor = conn.cursor()
cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
