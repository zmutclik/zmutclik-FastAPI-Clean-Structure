from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core import config
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import AuthBackend, AuthenticationMiddleware, SQLAlchemyMiddleware, LogsMiddleware
from core.exceptions import CustomException
from core.di import init_di

from core.db import dbcore_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from app._sys.crossorigin.domain import CrossOrigin

from api import router


def init_routers(app: FastAPI) -> None:
    app.include_router(router)


def init_cors(app: FastAPI) -> None:
    try:
        with dbcore_engine.begin() as connection:
            with Session(bind=connection) as db:
                result = db.execute(select(CrossOrigin)).all()
                allow_origins = []
                for item in result:
                    allow_origins.append(item)
                if allow_origins == []:
                    allow_origins.append("*")
                app.add_middleware(
                    CORSMiddleware,
                    allow_origins=allow_origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
    except:
        print("Koneksi Database Core Error : app->init_cors")


def init_listeners(app: FastAPI) -> None:
    # Exception handler
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
    app.add_middleware(
        AuthenticationMiddleware,
        backend=AuthBackend(),
        on_error=on_auth_error,
    )
    app.add_middleware(LogsMiddleware)


# def init_startup(app: FastAPI) -> None:
#     @app.on_event("startup")
#     async def startup_event():
#         await init_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title=config.APP_NAME,
        description=config.APP_DESCRIPTION,
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
    )
    init_routers(app=app)
    init_cors(app=app)
    init_listeners(app=app)
    init_middleware(app=app)
    # await init_startup(app=app)
    init_di()
    return app


app = create_app()
