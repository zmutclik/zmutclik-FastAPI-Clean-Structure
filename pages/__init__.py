from fastapi import FastAPI, Request
from .routers.auth import auth_router

###################################################################################################################
pages_app = FastAPI(
    title="Pages",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0.0",
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


__all__ = ["pages_app"]
