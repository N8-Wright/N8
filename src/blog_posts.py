import sqlite3
from datetime import datetime
from time import mktime
from typing import Generator
from uuid import uuid4, UUID
from blog_post import BlogPost

class BlogPosts:
    def __init__(self, db_path):
        self.db_path = db_path
        db_connection = sqlite3.connect(db_path)
        cursor = db_connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS posts(id BLOB PRIMARY KEY, created_date INTEGER, modified_date INTEGER, content TEXT, name TEXT)")
        db_connection.close()
    
    def create_post(self, name: str, content: str) -> UUID:
        db_connection = sqlite3.connect(self.db_path)
        cursor = db_connection.cursor()
        
        now = datetime.now()
        unix_now = mktime(now.timetuple())

        new_id = uuid4()
        cursor.execute("INSERT INTO posts VALUES(?, ?, ?, ?, ?)", (new_id.bytes, unix_now, unix_now, content, name))
        db_connection.commit()
        db_connection.close()
        return new_id
    
    def update_post(self, id: UUID, name: str, content: str) -> None:
        db_connection = sqlite3.connect(self.db_path)
        cursor = db_connection.cursor()
    
        now = datetime.now()
        unix_now = mktime(now.timetuple())
        cursor.execute("UPDATE posts SET modified_date=? WHERE id=?", (unix_now, id.bytes, ))
        cursor.execute("UPDATE posts SET content=? WHERE id=?", (content, id.bytes, ))
        cursor.execute("UPDATE posts SET name=? WHERE id=?", (name, id.bytes, ))
        db_connection.commit()
        db_connection.close()

    def get_post(self, id: UUID) -> BlogPost | None:
        db_connection = sqlite3.connect(self.db_path)
        cursor = db_connection.cursor()
        post = cursor.execute("SELECT * FROM posts WHERE id=?", (id.bytes, )).fetchone()
        db_connection.close()
        if post != None:
            return BlogPost(id, datetime.fromtimestamp(post[1]), datetime.fromtimestamp(post[2]), post[3], post[4])
        
        return None
    
    def get_posts(self) -> list[BlogPost]:
        db_connection = sqlite3.connect(self.db_path)
        cursor = db_connection.cursor()
        res = cursor.execute("SELECT * FROM posts")
        
        posts = res.fetchall()
        result = []
        for post in posts:
            result.append(BlogPost(UUID(bytes=post[0]), datetime.fromtimestamp(post[1]), datetime.fromtimestamp(post[2]), post[3], post[4]))
        
        db_connection.close()
        return result
        
