from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from core.exceptions import TokenExpiredException


class RedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except TokenExpiredException as e:
            return e.get_redirect_response()
