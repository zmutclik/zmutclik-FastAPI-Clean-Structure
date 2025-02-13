from starlette.responses import RedirectResponse
from fastapi import HTTPException


class RequiresLoginException(Exception):
    def __init__(self, redirect_uri: str = "/auth/loggedin"):
        self.redirect_uri = redirect_uri


class TokenExpiredException(HTTPException):
    def __init__(self, redirect_uri: str = ""):
        self.redirect_uri = redirect_uri
        super().__init__(status_code=401, detail="Token expired. Redirecting to refresh.")

    def get_redirect_response(self):
        return RedirectResponse(url="/auth/refresh?redirect_uri=" + self.redirect_uri)
