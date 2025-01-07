from fastapi import FastAPI, Request
from core import config
from ._auth import auth_router

###################################################################################################################
pages_app = FastAPI(
    title=config.APP_NAME + " [ Pages ]",
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    redoc_url=None,
)

### Sub FastAPI ###
pages_app.include_router(auth_router)


# ###################################################################################################################
from fastapi.responses import RedirectResponse
from core.exceptions import RequiresLoginException


@pages_app.exception_handler(RequiresLoginException)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(_.nextRouter)


from core.exceptions import CustomException
from fastapi.responses import JSONResponse


@pages_app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


__all__ = ["pages_app"]
