from datetime import datetime
from typing import Annotated
import uuid
from fastapi import Depends, FastAPI, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from authentication import require_auth
from blog_post import BlogPost
from settings import Settings
from mistletoe import markdown
from blog_posts import BlogPosts

g_settings = Settings()
posts = BlogPosts("blogs.db")
app = FastAPI()
security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

@app.get("/")
def read_root(request: Request):
    id = posts.create_post("Testing 1234")
    posts.update_post(id, "12345")
    post = posts.get_post(id)
    rendered = markdown("# Hello")

    return templates.TemplateResponse(
        request=request, name="basic_page.html", context={"body": rendered}
    )

@app.get("/admin/posts")
def read_admin_pages(request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    posts = [BlogPost(uuid.uuid4(), datetime.now(), datetime.now(), "Testing")]

    return templates.TemplateResponse(
        request=request, name="admin_posts.html", context={"posts": posts}
    )

@app.get("/admin/edit/{id}")
def read_admin_post(id: uuid.UUID, request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    posts = [BlogPost(uuid.uuid4(), datetime.now(), datetime.now(), "Testing")]

    rendered = markdown("# Hello")
    return templates.TemplateResponse(
        request=request, name="basic_page.html", context={"body": rendered}
    )
