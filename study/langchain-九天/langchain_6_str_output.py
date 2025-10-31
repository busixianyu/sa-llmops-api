import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

load_dotenv(override=True)

model = init_chat_model(model="deepseek-r1:1.5b", model_provider="ollama")

question = "请问，你叫什么名字?"

basic_qa_chain = model | StrOutputParser()

print(basic_qa_chain.invoke(question))

