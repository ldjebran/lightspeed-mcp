import httpx
from urllib.parse import urljoin

from mcp.server.fastmcp.utilities.logging import get_logger

from lightspeed_mcp.authentication.context import auth_context_var

logger = get_logger(__name__)


async def fetch_current_user_data() -> str:
    """return the current logged-in AAP user information"""
    auth_user = auth_context_var.get()

    auth_headers = auth_user.authentication_info.get_headers() if auth_user else {}
    server_url = auth_user.authentication_info.server_url if auth_user else None
    verify_cert = auth_user.authentication_info.verify_cert if auth_user else True

    async with httpx.AsyncClient(verify=verify_cert) as client:
        response = await client.get(
            urljoin(server_url, "/api/gateway/v1/me/"), headers=auth_headers
        )
        return response.text
