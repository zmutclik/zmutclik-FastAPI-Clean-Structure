from fastapi import FastAPI, Request
from core import config
from ._auth import auth_router
from ._system import system_router

#######################################################################################################################
pages_app = FastAPI(
    title=config.APP_NAME + " [ Pages ]",
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    # swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    redoc_url=None,
)

### Sub FastAPI ###
pages_app.include_router(auth_router)
pages_app.include_router(system_router)


#######################################################################################################################
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
from core.exceptions import RequiresLoginException
from core.exceptions import CustomException
from fastapi.exceptions import RequestValidationError


@pages_app.exception_handler(RequiresLoginException)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(_.nextRouter)


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

    content = {"error_code": status.HTTP_422_UNPROCESSABLE_ENTITY, "message": "request validation error", "detail": jsonable_encoder(modified_details)}
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=content,
    )


__all__ = ["pages_app"]
