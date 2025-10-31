import os

from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi

load_dotenv(override=True)

model = ChatTongyi(model="qwen-plus-latest", api_key=os.getenv("DASHSCOPE_API_KEY"))

question = "请问，你叫什么名字?"

result = model.invoke(question)

print(result.content)

