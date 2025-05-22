from mcp.server.fastmcp import FastMCP

from lightspeed_mcp.sample_aap_tool import fetch_current_user_data


def register_sample_tools(mcp: FastMCP):
    mcp.add_tool(fetch_current_user_data)
