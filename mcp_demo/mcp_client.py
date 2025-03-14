# mcp_client.py
from mcp.client.sse import sse_client
from typing import Any

class EnhancedClient:
    def __init__(self, server_url: str):
        self.client = sse_client(server_url)
        
    async def list_tools(self) -> list[dict]:
        """获取服务器工具列表"""
        return await self.client.discover()
    
    async def call_tool(self, tool_name: str, params: dict) -> Any:
        """调用远程工具"""
        return await self.client.call_tool(tool_name, arguments=params)