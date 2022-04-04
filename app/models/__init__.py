import psycopg2
from os import getenv

configs = {
    "host": getenv("DB_HOST"),
    "database": getenv("DB_DATABASE"),
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASSWORD"),
}


def conn_cur():
    conn = psycopg2.connect(**configs)
    cur = conn.cursor()

    return conn, cur


def commit_close(conn, cur, commit=True):
    conn.commit()
    cur.close()
    conn.close()
