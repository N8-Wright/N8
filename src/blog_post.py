from datetime import datetime
from uuid import UUID
class BlogPost:
    created_date: datetime
    modified_date: datetime
    content: str
    id: UUID
    name: str

    def __init__(self, id: UUID, created_date: datetime, modified_date: datetime, content: str, name: str):
        self.id = id
        self.created_date = created_date
        self.modified_date = modified_date
        self.content = content
        self.name = name
        