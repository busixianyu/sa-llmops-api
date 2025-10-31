import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field

load_dotenv(override=True)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="你叫小帅，是一个乐于助人的助手"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

model = init_chat_model(model="deepseek-r1:1.5b", model_provider="ollama")

messages_list = [
    HumanMessage(content="你好，我叫陈明，好久不见。"),
    AIMessage(content="你好，我是小帅，很高兴认识你"),
]
question = "你叫什么名字？"

messages_list.append(HumanMessage(content=question))

basic_chain = chat_prompt | model | StrOutputParser()

print(basic_chain.invoke({"messages": messages_list}))