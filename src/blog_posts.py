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

from datetime import datetime
from time import mktime
from uuid import uuid4, UUID
from blog_post import BlogPost
from sqlite_helpers import connect_with_wal, connection, transaction

class BlogPosts:
    def __init__(self, db_path):
        self.db_path = db_path
        with connection(db_path) as db_connection:     
            cursor = db_connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS posts(id BLOB PRIMARY KEY, created_date INTEGER, modified_date INTEGER, content TEXT, name TEXT)")
    
    def create_post(self, name: str, content: str) -> UUID:
        now = datetime.now()
        unix_now = mktime(now.timetuple())
        new_id = uuid4()
        with connection(self.db_path) as db_connection:
            with transaction(db_connection) as cursor:
                cursor.execute("INSERT INTO posts VALUES(?, ?, ?, ?, ?)", (new_id.bytes, unix_now, unix_now, content, name))

        return new_id
    
    def update_post(self, id: UUID, name: str, content: str) -> None:
        now = datetime.now()
        unix_now = mktime(now.timetuple())
        with connection(self.db_path) as db_connection:
            with transaction(db_connection) as cursor:
                cursor.execute("UPDATE posts SET modified_date=? WHERE id=?", (unix_now, id.bytes, ))
                cursor.execute("UPDATE posts SET content=? WHERE id=?", (content, id.bytes, ))
                cursor.execute("UPDATE posts SET name=? WHERE id=?", (name, id.bytes, ))

    def get_post(self, id: UUID) -> BlogPost | None:
        with connection(self.db_path) as db_connection:
            cursor = db_connection.cursor()
            post = cursor.execute("SELECT * FROM posts WHERE id=?", (id.bytes, )).fetchone()
            if post != None:
                return BlogPost(id, datetime.fromtimestamp(post[1]), datetime.fromtimestamp(post[2]), post[3], post[4])
            
        return None
    
    def get_posts(self) -> list[BlogPost]:
        posts = []
        with connection(self.db_path) as db_connection:
            cursor = db_connection.cursor()
            res = cursor.execute("SELECT * FROM posts ORDER BY created_date DESC")
            posts = res.fetchall()
        
        result = []
        for post in posts:
            result.append(BlogPost(UUID(bytes=post[0]), datetime.fromtimestamp(post[1]), datetime.fromtimestamp(post[2]), post[3], post[4]))
        
        return result
    
    def get_latest_posts(self) -> list[BlogPost]:
        posts = []
        with connection(self.db_path) as db_connection:
            cursor = db_connection.cursor()
            res = cursor.execute("SELECT * FROM posts ORDER BY created_date DESC LIMIT 5")
            posts = res.fetchall()
        
        result = []
        for post in posts:
            result.append(BlogPost(UUID(bytes=post[0]), datetime.fromtimestamp(post[1]), datetime.fromtimestamp(post[2]), post[3], post[4]))
        
        return result
        
