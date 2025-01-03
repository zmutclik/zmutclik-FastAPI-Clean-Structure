from time import sleep
from datetime import datetime

from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse, PlainTextResponse
from sqlalchemy.orm import Session
from pages.base import templates

login_router = APIRouter()


@login_router.get("", response_class=HTMLResponse)
def form_login(
    request: Request,
    next: str = None,
):
    return templates.TemplateResponse(
        request=request,
        name="pages/auth/login/login.html",
        context={"nextpage": next},
    )
