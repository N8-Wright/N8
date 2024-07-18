﻿from typing import Annotated
from uuid import UUID
from fastapi import Depends, FastAPI, Request, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response
from authentication import require_auth
from settings import Settings
from mistletoe import markdown
from blog_posts import BlogPosts
from starlette import status

g_settings = Settings()
posts = BlogPosts("blogs.db")
app = FastAPI()
security = HTTPBasic()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

@app.get("/")
def read_root(request: Request):
    blog_posts = posts.get_latest_posts()

    return templates.TemplateResponse(
        request=request, name="home.html", context={"posts": blog_posts}
    )

@app.get("/posts/{id}")
def get_post(id: UUID, request: Request):
    post = posts.get_post(id)
    if post == None:
        return Response(status_code=404)
    
    rendered = markdown(post.content)
    return templates.TemplateResponse(
        request=request, name="basic_page.html", context={"body": rendered}
    )

@app.get("/admin/posts")
def read_admin_pages(request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    blog_posts = posts.get_posts()

    return templates.TemplateResponse(
        request=request, name="admin_posts.html", context={"posts": blog_posts}
    )

@app.get("/admin/edit/{id}")
def read_admin_post(id: UUID, request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    post = posts.get_post(id)
    if post != None:
        return templates.TemplateResponse(
            request=request, name="edit_post.html", context={"body": post.content, "post_id": id, "post_name": post.name }
        )

@app.get("/admin/create_post")
def get_create_post_page(request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)

    return templates.TemplateResponse(
        request=request, name="create_post.html"
    )

@app.post("/admin/post/update/{id}")
def update_post(id: UUID, post_name: Annotated[str, Form()], post_content: Annotated[str, Form()], request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    posts.update_post(id, post_name, post_content)
    post = posts.get_post(id)
    rendered = markdown(post.content)

    return templates.TemplateResponse(
        request=request, name="basic_page.html", context={"body": rendered}
    )

@app.post("/admin/post/create")
async def create_post(post_name: Annotated[str, Form()],
                      post_content: Annotated[str, Form()],
                      credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    id = posts.create_post(post_name, post_content) 
    return RedirectResponse(app.url_path_for("get_post", id=id), status_code=status.HTTP_302_FOUND)
