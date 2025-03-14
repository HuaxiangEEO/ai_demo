# 此脚本实现了一个支持 MCP 协议的服务器：
# 提供了一个名为 example-prompt 的 prompt
# 支持客户端通过标准输入/输出与服务器通信
# 能够响应客户端的 list_prompts 和 get_prompt 请求，返回相应的内容


# Server 提供服务器实例化功能
# NotificationOptions 用于配置通知选项
from mcp.server import Server, NotificationOptions
# 服务器初始化时的选项
from mcp.server.models import InitializationOptions
# 提供标准输入/输出支持，用于与外部工具交互
import mcp.server.stdio
# 定义与 mcp 协议相关的类型
import mcp.types as types
import asyncio
from translate import Translator




# 创建一个名为 example-server 的服务器实例
server = Server("example-server")

# 注册一个回调函数，返回服务器支持的 prompt 列表
@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        # 添加加法工具的 prompt
        types.Prompt(
            name="add-numbers",
            description="一个简单的加法工具，可以计算两个数字的和",
            arguments=[
                types.PromptArgument(
                    name="number1",
                    description="第一个数字",
                    required=True
                ),
                types.PromptArgument(
                    name="number2",
                    description="第二个数字",
                    required=True
                )
            ]
        ),
        # 添加中译英工具的 prompt
        types.Prompt(
            name="translate-to-english",
            description="将中文文本翻译成英语",
            arguments=[
                types.PromptArgument(
                    name="chinese_text",
                    description="需要翻译的中文文本",
                    required=True
                )
            ]
        )
    ]


# 注册一个回调函数，用于根据 prompt 名称和参数生成具体的 prompt 内容
@server.get_prompt()
async def handle_get_prompt(
    name: str,
    arguments: dict[str, str] | None
) -> types.GetPromptResult:
    if name == "add-numbers":
        if not arguments or "number1" not in arguments or "number2" not in arguments:
            raise ValueError("必须提供两个数字参数")
        
        try:
            num1 = float(arguments["number1"])
            num2 = float(arguments["number2"])
            result = num1 + num2
            
            return types.GetPromptResult(
                description="计算两个数字的和",
                messages=[
                    types.PromptMessage(
                        role="assistant",
                        content=types.TextContent(
                            type="text",
                            text=f"计算结果：{num1} + {num2} = {result}"
                        )
                    )
                ]
            )
        except ValueError:
            raise ValueError("输入的参数必须是有效的数字")
    elif name == "translate-to-english":
        if not arguments or "chinese_text" not in arguments:
            raise ValueError("必须提供中文文本")
        
        try:
            chinese_text = arguments["chinese_text"]
            # 设置翻译方向：中文(zh) -> 英文(en)
            translator = Translator(from_lang="zh", to_lang="en")
            english_text = translator.translate(chinese_text)

            return types.GetPromptResult(
                description="中文翻译为英语",
                messages=[
                    types.PromptMessage(
                        role="assistant",
                        content=types.TextContent(
                            type="text",
                            text=f"原文：{chinese_text}\n译文：{english_text}"
                        )
                    )
                ]
            )
        except Exception as e:
            raise ValueError(f"翻译过程中出现错误：{str(e)}")
    else:
        raise ValueError(f"Unknown prompt: {name}")


async def run():
    # 使用 stdio_server 启动标准输入/输出的服务器模式
    # 提供 read_stream 和 write_stream 用于数据传输
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        # 启动服务器，使用初始化选项 InitializationOptions
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="0.1.0",
                # 配置服务器功能，包括通知选项和实验性功能
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    # 使用 asyncio 运行异步的 run() 函数，启动服务器
    asyncio.run(run())