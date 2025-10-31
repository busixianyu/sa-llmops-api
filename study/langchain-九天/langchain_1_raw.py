import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com1")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role":"system", "content": "你是一个乐于助人的助手，请根据用户的问题给出答案"},
        {"role":"user", "content": "请介绍一下你自己"}
    ]
)
print(response.choices[0].message.content)