from typing import Union
from fastapi import FastAPI

from blog_posts import blog_posts

posts = blog_posts("blogs.db")
app = FastAPI()

@app.get("/")
def read_root():
    id = posts.create_post("Testing 1234")
    posts.update_post(id, "12345")
    post = posts.get_post(id)
    
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}