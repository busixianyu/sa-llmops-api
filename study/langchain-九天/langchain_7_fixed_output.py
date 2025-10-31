import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)

prompt_template = ChatPromptTemplate([
    ("system", "你是一个乐于助人的助手，请根据用户的问题给出答案"),
    ("user", "这是用户的问题：{topic}，请用'yes'或'no'来回答，并不要包含任何其他文字")
])

model = init_chat_model(model="deepseek-r1:1.5b", model_provider="ollama")

question = "请问，0+1是否大于2？"

basic_qa_chain = prompt_template | model | StrOutputParser()

print(basic_qa_chain.invoke({"topic": question}))

