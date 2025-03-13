# mcp_server.py
from mcp.server.fastmcp import FastMCP
import httpx

# 创建 MCP 服务器实例
app = FastMCP("demo-server")

# 注册数学计算工具
@app.tool()
def math_calculator(expression: str) -> float:
    """执行数学表达式计算，支持加减乘除"""
    return eval(expression)

# 注册天气查询工具
@app.tool()
async def get_weather(city: str) -> str:
    """获取城市天气信息"""
    async with httpx.AsyncClient() as client:
        return f"{city}天气：多云"

# 启动服务器（SSE模式）
if __name__ == "__main__":
    app.run(transport="sse")