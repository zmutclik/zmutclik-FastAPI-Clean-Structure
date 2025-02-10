from fastapi import FastAPI, Request

from .login import login_router
from .loggedin import loggedin_router
from .logout import logout_router
from .timeout import timeout_router
from .register import register_router
from .profile import profile_router
from .refresh import refresh_router

from core import config

#######################################################################################################################
pages_auth = FastAPI(
    title=config.APP_NAME + " [ AUTH ]",
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    # swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url=None if config.ENV == "production" else "/docs",
    redoc_url=None if config.ENV == "production" else "/redoc",
)

### Sub FastAPI ###
pages_auth.include_router(login_router)
pages_auth.include_router(loggedin_router)
pages_auth.include_router(logout_router)
pages_auth.include_router(timeout_router)
pages_auth.include_router(register_router)
pages_auth.include_router(profile_router)
pages_auth.include_router(refresh_router)


#######################################################################################################################
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
from core.exceptions import RequiresLoginException
from core.exceptions import CustomException
from fastapi.exceptions import RequestValidationError
from core.fastapi.middlewares import RedirectMiddleware


pages_auth.add_middleware(RedirectMiddleware)


@pages_auth.exception_handler(RequiresLoginException)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(_.nextRouter)


@pages_auth.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


@pages_auth.exception_handler(RequestValidationError)
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


__all__ = ["pages_auth"]
