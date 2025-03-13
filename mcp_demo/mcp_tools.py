from langchain.tools import tool
from mcp_client import EnhancedClient
from pydantic import BaseModel

client = EnhancedClient("http://localhost:8000")

class MathInput(BaseModel):
    expression: str = "2+3 * 4"

@tool(args_schema=MathInput)
def calculate(expression: str) -> float:
    """数学计算工具"""
    return client.call_tool("math_calculator", {"expression": expression})

class WeatherInput(BaseModel):
    city: str = "北京"

@tool(args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """天气查询工具""" 
    return client.call_tool("get_weather", {"city": city})