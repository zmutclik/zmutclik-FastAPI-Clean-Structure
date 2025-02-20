from fastapi import FastAPI, Request
from core import config
from core.pages.setting import pages_settings
from core.pages.system import pages_sys

from .dashboard import dashboard_router
from .documentation import documentation_router
from core.utils import remove_html_tags

#######################################################################################################################
pages_app = FastAPI(
    title=remove_html_tags(config.APP_NAME) + " [ Pages ]",
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    # swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    redoc_url=None,
)

### Sub FastAPI ###
pages_app.include_router(dashboard_router)
pages_app.include_router(documentation_router)

pages_app.mount("/settings", pages_settings)
pages_app.mount("/sys", pages_sys)


#######################################################################################################################
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
from core.exceptions import RequiresLoginException
from core.exceptions import CustomException
from fastapi.exceptions import RequestValidationError


@pages_app.exception_handler(RequiresLoginException)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(_.redirect_uri)


@pages_app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"error_code": exc.error_code, "message": exc.message},
    )


@pages_app.exception_handler(RequestValidationError)
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


__all__ = ["pages_app"]
