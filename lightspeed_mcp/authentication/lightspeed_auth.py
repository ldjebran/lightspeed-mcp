from typing import List

from starlette.authentication import (
    AuthCredentials,
    BaseUser,
    AuthenticationError,
)
from starlette.requests import HTTPConnection

from .protocols.backend import AuthenticationBackend
from .protocols.validator import AuthenticationValidator

from mcp.server.fastmcp.utilities.logging import get_logger

logger = get_logger(__name__)


class LightspeedAuthenticationBackend(AuthenticationBackend):
    def __init__(self, authentication_validators: List[AuthenticationValidator]):
        self._authentication_validators = authentication_validators

    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser] | None:
        logger.debug(">>>>>>  call authentication backend authenticate")
        authorization_header = conn.headers.get("Authorization", None)
        jwt_header = conn.headers.get("X-DAB-JW-TOKEN", None)
        logger.debug("header Authorization >>>>> %s ", authorization_header)
        logger.debug("header X-DAB-JW-TOKEN >>>>> %s ", jwt_header)
        for validator in self._authentication_validators:
            value = await validator.validate(conn)
            if value is not None:
                return value

        raise AuthenticationError(
            "Authentication failed, all authentication validators failed"
        )
