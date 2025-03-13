from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# 使用混元模型回答问题
def gen_txt_by_hunyuan(prompt):
    # 构造 client
    client = OpenAI(
        api_key=os.environ.get("HUNYUAN_API_KEY"), # 混元 APIKey
        base_url=os.environ.get("HUNYUAN_BASE_URL"), # 混元 endpoint
    )


    # 使用混元模型
    completion = client.chat.completions.create(
        model="hunyuan-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            },
        ],
        extra_body={
            "enable_enhancement": True, # <- 自定义参数
        },
    )

    print(completion.choices[0].message.content)

# 使用千问模型回答问题
def gen_txt_by_qwen(prompt):
    # 构造 client
    client = OpenAI(
        api_key=os.environ.get("DASHSCOPE_API_KEY"), # 通义千问 APIKey
        base_url=os.environ.get("DASHSCOPE_BASE_URL"), # 通义千问 endpoint
    )
    
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
            ]
    )
    print(completion.choices[0].message.content)


# 向小学生讲解数学问题
def explain_math_for_primary_student(prompt):
    # 构造 client
    client = OpenAI(
        api_key=os.environ.get("SILICON_API_KEY"), # 硅基流动 APIKey
        base_url=os.environ.get("SILICON_BASE_URL"), # 硅基流动 endpoint
    )
    # 使用gpt-4o模型
    completion = client.chat.completions.create(
        model="Qwen/QwQ-32B",
        messages=[
            {"role": "system", "content": "你是一个数学老师，善于给小学生讲解数学问题."},
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    print(completion.choices[0].message.content)


if __name__ == "__main__":
    # gen_txt_by_hunyuan("你好")
    # gen_txt_by_qwen("How do I check if a Python object is an instance of a class?")
    explain_math_for_primary_student("什么是勾股定理")

