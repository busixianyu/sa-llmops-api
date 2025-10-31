import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv(override=True)

prompt_template = ChatPromptTemplate([
    ("system", "你是一个乐于助人的助手，请根据用户的问题给出答案"),
    ("user", "请根据以下内容提取用户信息，并返回一个json格式：\n{input}\n\n{format_instructions}")
])

class UserInfo(BaseModel):
    name: str = Field(description="用户姓名")
    age: int = Field(description="用户年龄")

parser = PydanticOutputParser(pydantic_object=UserInfo)
model = init_chat_model(model="deepseek-r1:1.5b", model_provider="ollama")

question = "用户叫李雷，今年35岁，是一名程序员"

basic_qa_chain = prompt_template.partial(format_instructions=parser.get_format_instructions()) | model | StrOutputParser()
print(parser.get_format_instructions())
print(basic_qa_chain.invoke({"input": question}))

