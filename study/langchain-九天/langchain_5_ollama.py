import os

from dotenv import load_dotenv
from langchain_ollama.chat_models import ChatOllama

load_dotenv(override=True)

model = ChatOllama(model="deepseek-r1:1.5b")

question = "请问，你叫什么名字?"

result = model.invoke(question)

print(result.content)

