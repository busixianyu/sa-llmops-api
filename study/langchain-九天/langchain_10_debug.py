import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field

load_dotenv(override=True)

news_prompt = ChatPromptTemplate.from_template(template="请根据以下新闻标题撰写一段简短的新闻内容（100字以内）：\n\n标题：{title}")

model = init_chat_model(model="deepseek-r1:1.5b", model_provider="ollama")

news_chain = news_prompt | model

class News(BaseModel):
    title: str = Field("标题")
    location: str = Field("地点")
    event: str = Field("事件")

parser = PydanticOutputParser(pydantic_object=News)

summary_prompt = ChatPromptTemplate.from_template("请从下面这段新闻内容中提取关键信息，并返回结构化JSON格式：\n\n{content}\n\n{format_instructions}").partial(format_instructions=parser.get_format_instructions())

def debug_print(x):
    print("中间结果：", x)
    return x

debug_node = RunnableLambda(debug_print)

summary_chain = summary_prompt | model | parser

full_chain = news_chain | debug_node | summary_chain
print(full_chain.invoke({"title": "中国女足夺冠"}))