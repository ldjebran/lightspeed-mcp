from typing import Protocol, runtime_checkable

from starlette.requests import HTTPConnection
from starlette.authentication import AuthCredentials, BaseUser


@runtime_checkable
class AuthenticationValidator(Protocol):
    async def validate(
        self, connection: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser] | None: ...
