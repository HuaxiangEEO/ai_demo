from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的变量


@tool
def web_loader(url: str) -> str:
    """抓取url对应网页的内容"""
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs[0].page_content

llm = ChatOpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL"),
    model="deepseek-ai/DeepSeek-R1"
)

tools = [web_loader]
llm_with_tools = llm.bind_tools(tools)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个擅长对长文做总结的智能助手，可以精确提炼出长文中的要点。注意，请使用markdown格式返回结果。",
        ),
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm_with_tools, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

res = agent_executor.invoke(
    {
        "input": "这个链接讲了什么内容？ https://blog.csdn.net/xindoo/article/details/138356308?spm=1001.2014.3001.5501"
    }
)

print(res)
