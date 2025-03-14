# mcp_agent.py
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from mcp_tools import calculate, get_weather
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件中的变量

llm = ChatOpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL"),
    model="deepseek-ai/DeepSeek-R1"
)

system_message = """
你是一个专业计算助手，请按步骤执行：
1. 解析用户问题中的数学表达式或城市名称
2. 调用对应工具获取结果
3. 用自然语言解释计算过程。
"""

print(system_message)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",system_message,
        ),
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# 初始化 Agent
agent = create_tool_calling_agent(
    tools=[calculate, get_weather],
    llm=llm,
    prompt=prompt
)

# 创建执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=[calculate, get_weather],
    verbose=True
)

# 使用示例
response = agent_executor.invoke({
    "input": "请先计算(25+17)*3，然后告诉我杭州的天气"
})
print(response["output"])

