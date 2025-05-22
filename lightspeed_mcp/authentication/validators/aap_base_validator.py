from urllib.parse import urljoin
import httpx

from lightspeed_mcp.authentication.protocols.validator import AuthenticationValidator

from lightspeed_mcp.authentication.auth_user import (
    AuthenticationUser,
    AuthenticationInfo,
)

from starlette.requests import HTTPConnection
from starlette.authentication import (
    AuthCredentials,
    AuthenticationError,
    BaseUser,
)

from mcp.server.fastmcp.utilities.logging import get_logger

from lightspeed_mcp.authentication.context import auth_context_var

logger = get_logger(__name__)


class AAPBaseValidator(AuthenticationValidator):
    AUTHENTICATION_HEADER_NAME: str

    def __init__(self, authentication_server_url: str, verify_cert: bool = True):
        self._authentication_server_url = authentication_server_url
        self._verify_cert = verify_cert

    async def validate(
        self, connection: HTTPConnection
    ) -> tuple[AuthCredentials, BaseUser] | None:
        authentication_header_value = connection.headers.get(
            self.AUTHENTICATION_HEADER_NAME, None
        )
        if authentication_header_value is None:
            return None
        url = urljoin(self._authentication_server_url, "api/gateway/v1/me/")
        logger.debug("calling authentication server at url: %s", url)
        async with httpx.AsyncClient(verify=self._verify_cert) as client:
            response = await client.get(
                url=urljoin(self._authentication_server_url, "api/gateway/v1/me/"),
                headers=dict(Authorization=authentication_header_value),
            )
            if not response.is_success:
                logger.error(
                    "Authentication error occurred: status: %s, body: %s ",
                    response.status_code,
                    response.text,
                )
                response = response.status_code
                raise AuthenticationError("Authentication error failed")

        results = response.json()
        if len(results.get("results", [])) == 0:
            AuthenticationError("Authentication error, no user returned")

        auth_user = AuthenticationUser(
            results["results"][0]["username"],
            AuthenticationInfo(
                self.AUTHENTICATION_HEADER_NAME,
                authentication_header_value,
                self._authentication_server_url,
                verify_cert=self._verify_cert,
            ),
        )
        # set user to context var
        auth_context_var.set(auth_user)
        return AuthCredentials(), auth_user
