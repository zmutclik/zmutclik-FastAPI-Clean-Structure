from abc import ABC, abstractmethod
from typing import List

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from core.exceptions import CustomException, UnauthorizedException, RequiresLoginException


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List, exception=UnauthorizedException):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__
        self.exception = exception

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise self.exception


class RoleDependency(SecurityBase):
    def __init__(self, required_roles: str, exception=UnauthorizedException):
        self.required_roles = required_roles
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__
        self.exception = exception

    async def __call__(self, request: Request):
        if not self.required_roles in request.user.roles:
            raise self.exception


class ScopeDependency(SecurityBase):
    def __init__(self, required_scopes: list[str], exception=UnauthorizedException):
        self.required_scopes = required_scopes
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__
        self.exception = exception

    async def __call__(self, request: Request):
        if not all(roles in request.user.scopes for roles in self.required_scopes):
            raise self.exception


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return request.user.username is not None
