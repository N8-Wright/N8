from contextlib import contextmanager
from sqlite3 import Connection, Cursor
import sqlite3
from typing import Generator


def connect_with_wal(database: str) -> Connection:
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA temp_store=2")
    return conn

@contextmanager
def connection(database: str) -> Generator[Connection, Connection, Connection]:
    conn = connect_with_wal(database)
    try:
        yield conn
    finally:
        conn.close()
        
@contextmanager
def transaction(conn: Connection) -> Generator[Cursor, Cursor, Cursor]:
    try:
        yield conn.cursor()
    except:
        conn.rollback()
        raise
    else:
        conn.commit()