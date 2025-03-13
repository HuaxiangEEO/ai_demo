from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# client = OpenAI(
#     api_key=os.environ.get("SILICON_API_KEY"), # 硅基流动 APIKey
#     base_url=os.environ.get("SILICON_BASE_URL"), # 硅基流动 endpoint
# )
# model='deepseek-ai/DeepSeek-V2.5'

client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY"), # 通义千问 APIKey
    base_url=os.environ.get("DASHSCOPE_BASE_URL"), # 通义千问 endpoint
)
model='qwen-plus'

def add(a: float, b: float):
    return a + b

def mul(a: float, b: float):
    return a * b

def compare(a: float, b: float):
    if a > b:
        return f'{a} is greater than {b}'
    elif a < b:
        return f'{b} is greater than {a}'
    else:
        return f'{a} is equal to {b}'

def count_letter_in_string(a: str, b: str):
    string = a.lower()
    letter = b.lower()
    
    count = string.count(letter)
    return(f"The letter '{letter}' appears {count} times in the string.")


tools = [
{
    'type': 'function',
    'function': {
        'name': 'add',
        'description': 'Compute the sum of two numbers',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'int',
                    'description': 'A number',
                },
                'b': {
                    'type': 'int',
                    'description': 'A number',
                },
            },
            'required': ['a', 'b'],
        },
    }
}, 
{
    'type': 'function',
    'function': {
        'name': 'mul',
        'description': 'Calculate the product of two numbers',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'int',
                    'description': 'A number',
                },
                'b': {
                    'type': 'int',
                    'description': 'A number',
                },
            },
            'required': ['a', 'b'],
        },
    }
},
{
    'type': 'function',
    'function': {
        'name': 'count_letter_in_string',
        'description': 'Count letter number in a string',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'str',
                    'description': 'source string',
                },
                'b': {
                    'type': 'str',
                    'description': 'letter',
                },
            },
            'required': ['a', 'b'],
        },
    }
},
{
    'type': 'function',
    'function': {
        'name': 'compare',
        'description': 'Compare two number, which one is bigger',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'float',
                    'description': 'A number',
                },
                'b': {
                    'type': 'float',
                    'description': 'A number',
                },
            },
            'required': ['a', 'b'],
        },
    }
}
]

def call_func(messages):
    response = client.chat.completions.create(
        model=model,
        messages = messages,
        temperature=0.01,
        top_p=0.95,
        stream=False,
        tools=tools)

    # print("response:", response)
    return response

def function_call_playground(prompt):
    messages = [
        {'role': 'system', 'content': '你是一个AI助手。能够调用工具函数，并最终总结回答问题。请始终使用中文回答所有问题。即使问题是英文的，也要用中文回答。'},
        {'role': 'user', 'content': prompt}
    ]

    response = call_func(messages)    

    func_name = response.choices[0].message.tool_calls[0].function.name
    func_args = response.choices[0].message.tool_calls[0].function.arguments
    func_out = eval(f'{func_name}(**{func_args})') # 执行工具函数
    print("工具调用结果:", func_out)

    messages.append(response.choices[0].message)
    messages.append({
        'role': 'tool',
        'content': f'{func_out}',
        'tool_call_id': response.choices[0].message.tool_calls[0].id
    })
    # print("messages:", messages)
    
    response = call_func(messages)

    return response.choices[0].message.content
  
prompts = [
    "strawberry中有多少个r?", 
    "9.11和9.9，哪个小?"
]

for prompt in prompts:
    print(function_call_playground(prompt))