import asyncio
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from core import config
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    SQLAlchemyMiddleware,
    LogsMiddleware,
    SQLAlchemyAuthMiddleware,
    SQLAlchemyCoreMiddleware,
    SQLAlchemyMenuMiddleware,
)
from core.exceptions import CustomException
from core.di import init_di

from api import router
from pages import pages_app
from core.pages.auth import pages_auth


def init_routers(app: FastAPI) -> None:
    app.include_router(router)
    app.mount("/static", StaticFiles(directory="static", html=False), name="static")
    app.mount("/page", pages_app)
    app.mount("/auth", pages_auth)


def init_cors(app: FastAPI) -> None:
    print("allow_origins = ", config.ALLOW_ORIGINS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_listeners(app: FastAPI) -> None:
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def init_middleware(app: FastAPI) -> None:
    app.add_middleware(SQLAlchemyMiddleware)
    app.add_middleware(SQLAlchemyAuthMiddleware)
    app.add_middleware(SQLAlchemyCoreMiddleware)
    app.add_middleware(SQLAlchemyMenuMiddleware)
    app.add_middleware(LogsMiddleware)
    app.add_middleware(
        AuthenticationMiddleware,
        backend=AuthBackend(),
        on_error=on_auth_error,
    )


def create_app() -> FastAPI:
    app = FastAPI(
        title=config.APP_NAME,
        description=config.APP_DESCRIPTION,
        version=config.APP_VERSION,
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
    )
    init_routers(app=app)
    init_cors(app=app)
    init_listeners(app=app)
    init_middleware(app=app)
    init_di()
    return app


app = create_app()
