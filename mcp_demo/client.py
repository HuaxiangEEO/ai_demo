# 此脚本模拟了一个 mcp 客户端，通过标准输入/输出与服务器交互
# 执行的主要任务：
# 启动服务器
# 初始化客户端与服务器的连接
# 列出服务器支持的 prompts
# 获取一个具体的 prompt


# ClientSession 表示客户端会话，用于与服务器交互
# StdioServerParameters 定义与服务器的 stdio 连接参数
from mcp import ClientSession, StdioServerParameters
# 提供与服务器的 stdio 连接上下文管理器
from mcp.client.stdio import stdio_client
import asyncio



# 为 stdio 连接创建服务器参数
server_params = StdioServerParameters(
    # 服务器执行的命令，这里是 python
    command="python",
    # 启动命令的附加参数，这里是运行 server.py
    args=["server.py"],
    # 环境变量，默认为 None，表示使用当前环境变量
    # env=None
)


async def run():
    # 创建与服务器的标准输入/输出连接，并返回 read 和 write 流
    async with stdio_client(server_params) as (read, write):
        # 创建一个客户端会话对象，通过 read 和 write 流与服务器交互
        async with ClientSession(read, write) as session:
            # 向服务器发送初始化请求，确保连接准备就绪
            capabilities = await session.initialize()
            print("\n=== 服务器功能 ===")
            print("功能列表:", capabilities.capabilities)

            # 请求服务器列出所有支持的 prompt
            prompts_result = await session.list_prompts()
            print("\n=== 可用的 Prompts ===")         
 
            
            # 遍历并显示prompts
            for prompt in prompts_result.prompts:
                print(f"名称: {prompt.name}")
                print(f"描述: {prompt.description}")
                if prompt.arguments:
                    print("参数:")
                    for arg in prompt.arguments:
                        print(f"  - {arg.name}: {arg.description} (必需: {arg.required})")

            # 测试加法工具
            print("\n=== 测试加法工具 ===")
            # 测试用例 1: 整数相加
            add_result1 = await session.get_prompt("add-numbers", arguments={"number1": "10", "number2": "20"})
            print("整数相加:", add_result1.messages[0].content.text)

            # 测试用例 2: 小数相加
            add_result2 = await session.get_prompt("add-numbers", arguments={"number1": "3.14", "number2": "2.86"})
            print("小数相加:", add_result2.messages[0].content.text)

            try:
                # 测试用例 3: 错误输入处理
                await session.get_prompt("add-numbers", arguments={"number1": "abc", "number2": "123"})
            except Exception as e:
                print("错误处理测试:", str(e))

            # 测试翻译工具
            print("\n=== 测试翻译工具 ===")
            # 测试用例 1: 简单句子翻译
            translate_result1 = await session.get_prompt("translate-to-english", arguments={"chinese_text": "你好，世界"})
            print("简单句子翻译:", translate_result1.messages[0].content.text)

            # 测试用例 2: 复杂句子翻译
            translate_result2 = await session.get_prompt("translate-to-english", arguments={"chinese_text": "人工智能正在改变我们的生活方式"})
            print("复杂句子翻译:", translate_result2.messages[0].content.text)

            try:
                # 测试用例 3: 空输入处理
                await session.get_prompt("translate-to-english", arguments={})
            except Exception as e:
                print("翻译错误处理测试:", str(e))

if __name__ == "__main__":
    asyncio.run(run())