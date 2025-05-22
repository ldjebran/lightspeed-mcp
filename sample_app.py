from os import environ

from lightspeed_mcp.registry import register_sample_tools
from lightspeed_mcp.server import LightspeedAAPServer

from lightspeed_mcp.authentication import LightspeedAuthenticationBackend
from lightspeed_mcp.authentication.validators.aap_token_validator import (
    AAPTokenValidator,
)

from mcp.server.fastmcp.utilities.logging import configure_logging

configure_logging("DEBUG")

AAP_URL = environ.get("AAP_URL", "https://localhost")

mcp = LightspeedAAPServer(
    auth_backend=LightspeedAuthenticationBackend(
        authentication_validators=[
            AAPTokenValidator(AAP_URL, verify_cert=False),
        ]
    ),
    host="127.0.0.1",
    port=3180,
)


register_sample_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="sse")
