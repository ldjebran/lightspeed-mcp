from starlette.middleware.authentication import AuthenticationMiddleware

from starlette import status
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response


class LightspeedAuthenticationMiddleware(AuthenticationMiddleware):
    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        return PlainTextResponse(str(exc), status_code=status.HTTP_401_UNAUTHORIZED)
