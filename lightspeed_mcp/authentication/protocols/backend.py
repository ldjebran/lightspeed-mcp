from typing import Protocol, runtime_checkable

from starlette.authentication import AuthCredentials, BaseUser
from starlette.requests import HTTPConnection


@runtime_checkable
class AuthenticationBackend(Protocol):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser] | None: ...
