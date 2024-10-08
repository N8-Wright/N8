﻿# N8, An amalgamation of personal code
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

from typing import Annotated, Any
from uuid import UUID
from fastapi import Depends, FastAPI, Path, Request, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse, Response
from authentication import require_auth
from blog_post_comments import BlogPostComments
from settings import Settings
from mistletoe import markdown, HtmlRenderer
from blog_posts import BlogPosts
from starlette import status
from jinja2 import pass_context

g_settings = Settings()
posts = BlogPosts("blogs.db")
comments = BlogPostComments("blogs.db")

app = FastAPI()
security = HTTPBasic()

@pass_context
def urlx_for(context: dict, name: str, **path_params: Any, ) -> str:
    request: Request = context['request']
    http_url = request.url_for(name, **path_params)
    if scheme := request.headers.get('x-forwarded-proto'):
        return http_url.replace(scheme=scheme)
    return http_url

templates = Jinja2Templates(directory="templates/")
templates.env.globals['url_for'] = urlx_for

@app.get("/static/{path:path}")
async def static(path: str):
    if path != "output.css" and path != "spaghetti.js" and path != "me.jpg":
        return Response(status_code=404)
    
    response = FileResponse(f"static/{path}")
    response.headers["Cache-Control"] = "max-age=31536000"
    return response

@app.get("/")
def read_root(request: Request):
    blog_posts = posts.get_latest_posts()

    return templates.TemplateResponse(
        request=request, name="home.html", context={"posts": blog_posts}
    )

@app.get("/posts/{id}")
def get_post(id: UUID, request: Request):
    post = posts.get_post(id)
    post_comments = comments.get_comments(id)
    
    if post == None:
        return Response(status_code=404)
    
    rendered = markdown(post.content)
    return templates.TemplateResponse(
        request=request, name="basic_page.html", context={"post": post, "comments": post_comments, "body": rendered}
    )

@app.get("/comment/thanks")
def comment_thanks(request: Request):
    return templates.TemplateResponse(
        request=request, name="comment_thank_you.html"
    )
    
@app.post("/comment/{post_id}")
def add_comment(post_id: UUID, commenter: Annotated[str, Form(max_length=50)], comment: Annotated[str, Form(max_length=8192)], request: Request):
    comments.add_comment(post_id, commenter, comment)
    return RedirectResponse(app.url_path_for("comment_thanks"), status_code=status.HTTP_302_FOUND)
        
@app.get("/posts")
def get_posts(request: Request):
    all_posts = posts.get_posts()
    return templates.TemplateResponse(
        request=request, name="posts.html", context={"posts": all_posts}
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
    post_comments = comments.get_comments(id, show_only_visible=False)
    if post != None:
        return templates.TemplateResponse(
            request=request, name="edit_post.html", context={"body": post.content, "post": post, "comments": post_comments }
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
    return RedirectResponse(app.url_path_for("get_post", id=id), status_code=status.HTTP_302_FOUND)

@app.post("/admin/post/create")
async def create_post(post_name: Annotated[str, Form()],
                      post_content: Annotated[str, Form()],
                      credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    id = posts.create_post(post_name, post_content) 
    return RedirectResponse(app.url_path_for("get_post", id=id), status_code=status.HTTP_302_FOUND)

@app.post("/admin/post/delete/{id}")
def delete_post(id: UUID, request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    posts.delete_post(id)
    return RedirectResponse(app.url_path_for("read_admin_pages"), status_code=status.HTTP_302_FOUND)

@app.post("/admin/comment/delete")
def delete_comment(id: Annotated[UUID, Form()], request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    comment = comments.get_comment(id)
    comments.delete_comment(id)
    return RedirectResponse(app.url_path_for("get_post", id=comment.post_id), status_code=status.HTTP_302_FOUND)

@app.post("/admin/comment/visible")
def make_comment_visible(id: Annotated[UUID, Form()], request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    require_auth(g_settings, credentials)
    comment = comments.get_comment(id)
    comments.make_visible(id)
    return RedirectResponse(app.url_path_for("get_post", id=comment.post_id), status_code=status.HTTP_302_FOUND)

    