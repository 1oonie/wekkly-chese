import asyncio
import functools
import os
from typing import Union

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.templating import _TemplateResponse as TemplateResponse

app = Starlette(
    routes=[Mount("/static", StaticFiles(directory="static"), name="static")]
)

templates = Jinja2Templates("html")


def get_posts():
    posts = []
    path = "./static/articles"
    for file in os.listdir(path):
        if file.startswith("."):
            continue

        with open(path + "/" + file + "/author", "r") as fp:
            author = fp.read()
        with open(path + "/" + file + "/content", "r") as fp:
            content = fp.read()

        posts.append((author, file, content))
    return posts


@app.route("/", methods=["GET"])
async def home(request: Request) -> TemplateResponse:
    posts = await asyncio.get_event_loop().run_in_executor(None, get_posts)
    return templates.TemplateResponse(
        name="index.jinja2", context={"request": request, "posts": posts}
    )


def create_post(author: str, title: str, content: str):
    path = "./static/articles/" + title
    os.mkdir(path)
    with open(path + "/author", "w") as fp:
        fp.write(author)

    with open(path + "/content", "w") as fp:
        fp.write(content)


@app.route("/submit", methods=["GET", "POST"])
async def submit(request: Request) -> Union[TemplateResponse, RedirectResponse]:
    if request.method == "GET":
        return templates.TemplateResponse(
            name="submit.jinja2", context={"request": request}
        )
    else:
        form = await request.form()
        author, title, content = tuple(form.values())
        if not os.path.exists("./static/articles/" + title.lower()):
            await asyncio.get_event_loop().run_in_executor(
                None, functools.partial(create_post, author, title.lower(), content)
            )

            return RedirectResponse("/", status_code=303)
        else:
            return RedirectResponse(
                "/error",
                headers={"X-Error-Reason": "Article already exists!"},
                status_code=303,
            )


def get_post(name: str):
    path = "./static/articles/" + name + "/"
    with open(path + "author", "r") as fp:
        author = fp.read()
    with open(path + "content", "r") as fp:
        content = fp.read()

    return author, content


@app.route("/articles/{name}", methods=["GET"])
async def article(request: Request) -> Union[TemplateResponse, RedirectResponse]:
    name = request.path_params["name"].lower()
    if os.path.exists("./static/articles/" + name):
        author, content = await asyncio.get_event_loop().run_in_executor(
            None, functools.partial(get_post, name)
        )
        return templates.TemplateResponse(
            name="article.jinja2",
            context={
                "request": request,
                "title": name,
                "author": author,
                "content": content,
            },
        )
    else:
        return RedirectResponse(
            "/error",
            headers={"X-Error-Reason": "That article does not appear to exist..."},
            status_code=303,
        )


if __name__ == "__main__":
    uvicorn.run(app, port=8080)  # type: ignore
