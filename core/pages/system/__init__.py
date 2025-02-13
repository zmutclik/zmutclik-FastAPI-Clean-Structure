from fastapi import FastAPI, Request

from .menu import menu_router
from .scope import scope_router
from .repository import repository_router
from .logs import logs_router
from .coresetting import coresystem_router
from .session import session_router
from .message import message_router
from .clientsso import clientsso_router
from core import config

#######################################################################################################################
pages_sys = FastAPI(
    title=config.APP_NAME + " [ Pages / System ]",
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    # swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url=None if config.ENV == "production" else "/docs",
    redoc_url=None if config.ENV == "production" else "/redoc",
)

### Sub FastAPI ###
pages_sys.include_router(menu_router)
pages_sys.include_router(scope_router)
pages_sys.include_router(repository_router)
pages_sys.include_router(logs_router)
pages_sys.include_router(coresystem_router)
pages_sys.include_router(session_router)
pages_sys.include_router(message_router)
pages_sys.include_router(clientsso_router)


#######################################################################################################################
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
from core.exceptions import RequiresLoginException
from core.exceptions import CustomException
from fastapi.exceptions import RequestValidationError


@pages_sys.exception_handler(RequiresLoginException)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(_.redirect_uri)


@pages_sys.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


@pages_sys.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        modified_details.append(
            {
                "loc": error["loc"],
                "message": error["msg"],
                "type": error["type"],
            }
        )

    content = {
        "error_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "message": "request validation error",
        "detail": jsonable_encoder(modified_details),
    }
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content,
    )


@pages_sys.get("/")
async def page_system_check_error():
    raise ValueError("Ini error yang harusnya terlihat!")


__all__ = ["pages_sys"]
