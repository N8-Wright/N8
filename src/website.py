from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from authentication import require_auth
from settings import Settings
from blog_posts import BlogPosts

g_settings = Settings()
posts = BlogPosts("blogs.db")
app = FastAPI()
security = HTTPBasic()

@app.get("/")
def read_root():
    id = posts.create_post("Testing 1234")
    posts.update_post(id, "12345")
    post = posts.get_post(id)
    
    return {"Hello": "World"}

@app.get("/admin/posts")
def read_admin_page(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    return credentials.username
