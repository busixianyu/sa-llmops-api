import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_API_URL"),
)

completion = client.chat.completions.create(
    model="qwen-plus-latest",
    messages=[
        {"role": "system", "content": "你是一个乐于助人的助手。"},
        {"role": "user", "content": "请问，你叫什么名字?"},
    ],
)

print(completion.model_dump_json())