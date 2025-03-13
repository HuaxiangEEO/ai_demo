# mcp_agent.py
from langchain.agents import tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from mcp_tools import calculate, get_weather

# 初始化Agent
agent = tool_calling_agent.from_tools(
    tools=[calculate, get_weather],
    llm=ChatOpenAI(model="gpt-4", temperature=0),
    system_message="""你是一个专业计算助手，请按步骤执行：
    1. 解析用户问题中的数学表达式或城市名称
    2. 调用对应工具获取结果
    3. 用自然语言解释计算过程"""
)

# 创建执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=[calculate, get_weather],
    verbose=True
)

# 交互示例
response = agent_executor.invoke({
    "input": "请先计算(25+17)*3，然后告诉我杭州的天气"
})
print(response["output"])