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

from database import Database

d = Database("database.sqlite")

app = Starlette(
    routes=[Mount("/static", StaticFiles(directory="static"), name="static")],
    on_startup=[d.connect],
    on_shutdown=[d.disconnect],
)

templates = Jinja2Templates("html")


@app.route("/", methods=["GET"])
async def home(request: Request) -> TemplateResponse:
    posts = await d.connection.fetchall("SELECT * FROM articles;")
    return templates.TemplateResponse(
        name="index.jinja2", context={"request": request, "posts": posts}
    )


@app.route("/submit", methods=["GET", "POST"])
async def submit(request: Request) -> Union[TemplateResponse, RedirectResponse]:
    if request.method == "GET":
        return templates.TemplateResponse(
            name="submit.jinja2", context={"request": request}
        )
    else:
        form = await request.form()
        author, title, content = tuple(form.values())
        url_name = title.lower().replace(" ", "-")
        if not await d.connection.fetchone(
            "SELECT * FROM articles WHERE url_name=?;", url_name
        ):
            await d.connection.execute(
                "INSERT INTO articles(url_name, title, author, content) VALUES (?, ?, ?, ?);",
                url_name,
                title,
                author,
                content,
            )

            return RedirectResponse("/", status_code=303)
        else:
            return templates.TemplateResponse(
                name="error.jinja2", context={"request": request, "reason": "That article already exists!"}
            )


@app.route("/articles/{name}", methods=["GET"])
async def article(request: Request) -> Union[TemplateResponse, RedirectResponse]:
    name = request.path_params["name"].lower()
    if row := await d.connection.fetchone("SELECT * FROM articles WHERE url_name=?;", name):
        return templates.TemplateResponse(
            name="article.jinja2",
            context={
                "request": request,
                "title": row["title"],
                "author": row["author"],
                "content": row["content"],
            },
        )
    else:
        return templates.TemplateResponse(
            name="error.jinja2", context={"request": request, "reason": "That article does not exist."}
        )


if __name__ == "__main__":
    uvicorn.run(app, port=8080)  # type: ignore
