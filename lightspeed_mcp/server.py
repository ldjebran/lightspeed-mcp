from typing import Any

from lightspeed_mcp.authentication.protocols.backend import AuthenticationBackend
from lightspeed_mcp.authentication.middleware import LightspeedAuthenticationMiddleware

from mcp.server.fastmcp import FastMCP

from starlette.applications import Starlette

from mcp.server.fastmcp.utilities.logging import get_logger

logger = get_logger(__name__)


class LightspeedAAPServer(FastMCP):
    def __init__(
        self,
        auth_backend: AuthenticationBackend | None,
        **settings: Any,
    ):
        self._auth_backend = auth_backend
        super().__init__(name="Lightspeed AAP MCP", **settings)

    def init_app_authentication_backend(self, app: Starlette):
        if isinstance(self._auth_backend, AuthenticationBackend):
            logger.debug(">>>>>>>> register lightspeed AAP authentication backend")
            app.add_middleware(
                LightspeedAuthenticationMiddleware, backend=self._auth_backend
            )

    def sse_app(self, mount_path: str | None = None) -> Starlette:
        app = super().sse_app(mount_path=mount_path)
        self.init_app_authentication_backend(app)
        return app

    def streamable_http_app(self) -> Starlette:
        app = super().streamable_http_app()
        self.init_app_authentication_backend(app)
        return app
