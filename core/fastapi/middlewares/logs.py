import traceback
from fastapi import Request, Response
from core.app.logs.service import LogsService

from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send

from ...config import config


class LogsMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        logs = LogsService()
        request = await logs.start(request)

        response_body = b""  # Pastikan body dalam bentuk bytes
        response_status = 500
        response_headers = []
        traceerror = None

        async def send_wrapper(message):
            """Wrapper untuk menangkap response dari aplikasi."""
            nonlocal response_body, response_status, response_headers
            if message["type"] == "http.response.start":
                response_status = message["status"]
                response_headers.extend([(k.decode(), v.decode()) for k, v in message["headers"]])

            elif message["type"] == "http.response.body":
                response_body += message.get("body", b"")

        try:
            await self.app(scope, receive, send_wrapper)
            response_content = response_body if isinstance(response_body, bytes) else str(response_body).encode()

            response = Response(content=response_content, status_code=response_status)
            for k, v in response_headers:
                response.raw_headers.append((k.encode("latin-1"), v.encode("latin-1")))

        except Exception as e:
            from core.app.logs.schema import LogErrorSchema

            tb = traceback.extract_tb(e.__traceback__)  # Ambil traceback
            last_trace = tb[-1]  # Baris terakhir traceback (tempat error terjadi)

            traceerror = LogErrorSchema(
                error_type=e.__class__.__name__,
                error_message=str(e),
                error_traceback=traceback.format_exc(),
                file_name=last_trace.filename,
                line_number=str(last_trace.lineno),
                function_name=last_trace.name,
            )

            if config.DEBUG:
                print(traceerror.error_type, " : ", traceerror.error_message)
                print(f"📂 File: {traceerror.file_name}, line {traceerror.line_number}, in {traceerror.function_name}")
                # print(traceerror["error_traceback"])
            response = Response(content="Internal Server Error", status_code=500)

        logs.finish(request=request, response=response, traceerror=traceerror)
        await response(scope, receive, send)
