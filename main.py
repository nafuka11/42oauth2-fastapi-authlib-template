from __future__ import annotations

from typing import Any, Union

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import PlainTextResponse

from app.config import Settings
from app.oauth import ft_oauth

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=Settings().session_secret_key)

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def root(request: Request) -> Response:
    user = request.session.get("user")
    if user and user.get("login"):
        print(user)
        return templates.TemplateResponse(
            "index.html", {"request": request, "user": user}
        )
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login")
async def login(request: Request) -> Union[Any, RedirectResponse]:
    redirect_uri = request.url_for("callback")
    return await ft_oauth.authorize_redirect(request, redirect_uri)


@app.get("/callback")
async def callback(request: Request) -> RedirectResponse:
    token = await ft_oauth.authorize_access_token(request)
    res = await ft_oauth.get("me", token=token)
    user = res.json()
    request.session["user"] = {
        "login": user["login"],
        "level": user["cursus_users"][1]["level"],
    }
    return RedirectResponse(url="/")


@app.get("/logout")
async def logout(request: Request) -> RedirectResponse:
    request.session.pop("user", None)
    return RedirectResponse("/")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exception: StarletteHTTPException
) -> Response:
    return PlainTextResponse(str(exception.detail), status_code=exception.status_code)
