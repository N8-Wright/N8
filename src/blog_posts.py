import sqlite3
from datetime import datetime
from time import mktime
from uuid import uuid4, UUID
from blog_post import BlogPost

class BlogPosts:
    def __init__(self, db_path):
        self.db_path = db_path
        db_connection = sqlite3.connect(db_path)
        cursor = db_connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS posts(id BLOB PRIMARY KEY, created_date INTEGER, modified_date INTEGER, content TEXT)")
        db_connection.close()
    
    def create_post(self, content) -> UUID:
        db_connection = sqlite3.connect(self.db_path)
        cursor = db_connection.cursor()
        
        now = datetime.now()
        unix_now = mktime(now.timetuple())

        new_id = uuid4()
        cursor.execute("INSERT INTO posts VALUES(?, ?, ?, ?)", (new_id.bytes, unix_now, unix_now, content))
        db_connection.commit()
        db_connection.close()
        return new_id
    
    def update_post(self, id: UUID, content: str) -> None:
        db_connection = sqlite3.connect(self.db_path)
        cursor = db_connection.cursor()
    
        now = datetime.now()
        unix_now = mktime(now.timetuple())
        cursor.execute("UPDATE posts SET modified_date=? WHERE id=?", (unix_now, id.bytes, ))
        cursor.execute("UPDATE posts SET content=? WHERE id=?", (content, id.bytes, ))
        db_connection.commit()
        db_connection.close()

    def get_post(self, id: UUID) -> BlogPost | None:
        db_connection = sqlite3.connect(self.db_path)
        cursor = db_connection.cursor()
        post = cursor.execute("SELECT * FROM posts WHERE id=?", (id.bytes, )).fetchone()
        db_connection.close()
        if post != None:
            return BlogPost(id, datetime.fromtimestamp(post[1]), datetime.fromtimestamp(post[2]), post[3])
        
        return None
        
