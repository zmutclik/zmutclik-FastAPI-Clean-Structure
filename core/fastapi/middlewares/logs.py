from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app._sys.logs.service import LogsService


class LogsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logs = LogsService()
        request = await logs.create_logs(request)
        response = await call_next(request)
        logs.finish(request=request, response=response)
        return response
