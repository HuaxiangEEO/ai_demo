import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DASHSCOPE_API_KEY"), # 通义千问 APIKey
    base_url=os.environ.get("DASHSCOPE_BASE_URL"), # 通义千问 endpoint
)

completion = client.chat.completions.create(
    model="qwen-vl-ocr",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg",
                    "min_pixels": 28 * 28 * 4,
                    "max_pixels": 28 * 28 * 1280
                },
                # 为保证识别效果，目前模型内部会统一使用"Read all the text in the image."进行识别，用户输入的文本不会生效。
                {"type": "text", "text": "Read all the text in the image."},
            ]
        }
    ])

print(completion.choices[0].message.content)