from abc import ABC, abstractmethod
from typing import List

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from core.exceptions import CustomException, UnauthorizedException


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.username is not None


class HasRole(BasePermission):
    exception = UnauthorizedException

    def __init__(self, required_roles: List[str]):
        self.required_roles = required_roles

    async def has_permission(self, request: Request) -> bool:
        user_roles = request.user.roles
        if not user_roles:
            return False

        return all(roles in user_roles for roles in self.required_roles)


class HasScope(BasePermission):
    exception = UnauthorizedException

    def __init__(self, required_scopes: List[str]):
        self.required_scopes = required_scopes

    async def has_permission(self, request: Request) -> bool:
        user_scopes = request.user.scopes
        if not user_scopes:
            return False

        return all(scope in user_scopes for scope in self.required_scopes)
