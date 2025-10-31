import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv(override=True)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="你的名字叫小帅，是一个乐于助人的助手"),
        MessagesPlaceholder(variable_name="messages")
    ]
)

# model = ChatTongyi(model="qwen-plus-latest", api_key=os.getenv("DASHSCOPE_API_KEY"), verbose=True)
model = init_chat_model(model="deepseek-r1:1.5b", model_provider="ollama")
messages_list = []

chain = chat_prompt | model | StrOutputParser()

while True:
    user_input = input("User: ")
    if user_input == "exit":
        break
    messages_list.append(HumanMessage(content=user_input))
    assistant_response = chain.invoke({"messages": messages_list})
    print("Assistant: ", assistant_response)

    messages_list.append(AIMessage(content=assistant_response))
    messages_list = messages_list[-50:]
    print("Messages list: ", messages_list)
