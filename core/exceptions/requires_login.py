class RequiresLoginException(Exception):
    def __init__(self, nextRouter: str = "/auth/login"):
        self.nextRouter = nextRouter


from starlette.responses import RedirectResponse
from fastapi import HTTPException


class TokenExpiredException(HTTPException):
    def __init__(self, back_router: str = ""):
        self.backRouter = back_router
        super().__init__(status_code=401, detail="Token expired. Redirecting to refresh.")

    def get_redirect_response(self):
        return RedirectResponse(url="/auth/refresh?backRouter=" + self.backRouter)
