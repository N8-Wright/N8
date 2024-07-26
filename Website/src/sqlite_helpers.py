# N8, An amalgamation of personal code
# Copyright (C) 2024 Nathaniel Wright
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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