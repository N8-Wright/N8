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
from sqlite3 import Cursor
from time import mktime
from uuid import UUID, uuid4
from blog_post_comment import BlogPostComment
from sqlite_helpers import connection, transaction

class BlogPostComments:
    def __init__(self, db_path):
        self.db_path = db_path
        with connection(db_path) as db_connection:     
            cursor = db_connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS comments(id BLOB PRIMARY KEY, post_id BLOB, created_date INTEGER, content TEXT, commenter_name TEXT, visible BOOLEAN, FOREIGN KEY(post_id) REFERENCES posts(id))")
            
    def add_comment(self, post_id: UUID, commenter_name: str, comment: str):
        now = datetime.now()
        unix_now = mktime(now.timetuple())
        new_id = uuid4()
        
        with connection(self.db_path) as db_connection:
            with transaction(db_connection) as cursor:
                cursor.execute("INSERT INTO comments VALUES(?, ?, ?, ?, ?, ?)", (new_id.bytes, post_id.bytes, unix_now, comment, commenter_name, False))
    
    def get_comments(self, post_id: UUID, show_only_visible=True) -> list[BlogPostComment]:
        comments = []
        with connection(self.db_path) as db_connection:
            res = {}
            if show_only_visible:
                res = db_connection.execute("SELECT * FROM comments WHERE post_id=? AND visible=True ORDER BY created_date DESC", (post_id.bytes, ))
            else:
                res = db_connection.execute("SELECT * FROM comments WHERE post_id=? ORDER BY created_date DESC", (post_id.bytes, ))
                
            comments = res.fetchall()
            
        result = []
        for comment in comments:
            result.append(BlogPostComment(id=UUID(bytes=comment[0]),
                                          post_id=UUID(bytes=comment[1]),
                                          created_date=datetime.fromtimestamp(comment[2]),
                                          comment=comment[3],
                                          commenter=comment[4],
                                          visible=comment[5]))
        
        return result
    
    def get_comment(self, id: UUID) -> BlogPostComment:
        with connection(self.db_path) as db_connection:
            comment = db_connection.execute("SELECT * FROM comments where id=?", (id.bytes, )).fetchone()
            return BlogPostComment(id=UUID(bytes=comment[0]),
                post_id=UUID(bytes=comment[1]),
                created_date=datetime.fromtimestamp(comment[2]),
                comment=comment[3],
                commenter=comment[4],
                visible=comment[5])
            
    def delete_comment(self, id: UUID):
         with connection(self.db_path) as db_connection:
            with transaction(db_connection) as cursor:
                cursor.execute("DELETE FROM comments WHERE id=?", (id.bytes, ))
                
    def make_visible(self, id: UUID):
        with connection(self.db_path) as db_connection:
            with transaction(db_connection) as cursor:
                cursor.execute("UPDATE comments SET visible=True WHERE id=?", (id.bytes, ))
            