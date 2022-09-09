import json
from datetime import datetime

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates, _TemplateResponse

app = Starlette(
    routes=[
        Mount("/static", StaticFiles(directory="static", html=True), name="static"),
        Mount("/articles", StaticFiles(directory="articles", html=True), name="articles")
    ],
)

templates = Jinja2Templates("html")


@app.route("/", methods=["GET"])
async def root(request: Request) -> _TemplateResponse:
    with open("posts.json") as f:
        posts = json.loads(f.read())

    content = "<ul>" + "\n".join(
        f"<li><a href=\"/{post['timestamp']}/{post['url_name']}\">"
        f"{datetime.fromtimestamp(post['timestamp']).strftime('%d-%m-%Y')} - {post['name']}</a></li>"
        for post in posts
    ) + "</ul>"

    return templates.TemplateResponse(
        "base.jinja2", {"request": request, "title": "Homepage", "content": content}
    )

@app.route("/{timestamp}/{url_name}", methods=["GET"])
async def article(request: Request) -> _TemplateResponse:
    with open("posts.json") as f:
        posts = json.loads(f.read())

    content = "<p>The magical hamsters have run around in circles</p>"
    title = "(They are strong)"

    try:
        timestamp = int(request.path_params["timestamp"])
    except ValueError:
        return templates.TemplateResponse(
            "base.jinja2", {"request": request, "title": title, "content": content}
        )

    for post in posts:
        if post["timestamp"] == timestamp:
            with open(post["file"]) as f:
                content = f.read()
                title = post["name"]
                break

    return templates.TemplateResponse(
        "base.jinja2", {"request": request, "title": title, "content": content}
    )

@app.route("/json", methods=["GET"])
async def posts(request: Request) -> Response:
    with open("posts.json") as f:
        posts = f.read()
    return Response(posts, 200, media_type="application/json")


if __name__ == "__main__":
    uvicorn.run(app, port=8080)  # type: ignore
