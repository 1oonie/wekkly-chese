import uvicorn

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates, _TemplateResponse as TemplateResponse

app = Starlette(routes=[
    Mount("/static", StaticFiles(directory="static"), name="static")
])

templates = Jinja2Templates("html")

@app.route("/", methods=["GET"])
async def home(request: Request) -> TemplateResponse:
    return templates.TemplateResponse(name="index.jinja2", context={"request": request})

@app.route("/submit", methods=["GET", "POST"])
async def submit(request: Request) -> TemplateResponse:
    return templates.TemplateResponse(name="submit.jinja2", context={"request": request})

if __name__ == "__main__":
    uvicorn.run(app, port=8080) # type: ignore