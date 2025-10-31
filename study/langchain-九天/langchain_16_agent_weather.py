import os

from dotenv import load_dotenv
from langchain.agents.output_parsers import ToolsAgentOutputParser
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser
import requests
import json
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv(override=True)


@tool
def get_weather(loc):
    """
    查询即时天气函数
    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称，\
    注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，则loc参数需要输入'Beijing'；
    :return：OpenWeather API查询即时天气的结果，具体URL请求地址为：https://api.openweathermap.org/data/2.5/weather\
    返回结果对象类型为解析之后的JSON格式对象，并用字符串形式进行表示，其中包含了全部重要的天气信息
    """
    # Step 1.构建请求
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Step 2.设置查询参数
    params = {
        "q": loc,
        "appid": os.getenv("WEATHER_API_KEY"),  # 输入API key
        "units": "metric",  # 使用摄氏度而不是华氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }

    # Step 3.发送GET请求
    response = requests.get(url, params=params)

    # Step 4.解析响应
    data = response.json()
    return json.dumps(data)


prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个天气助手，请根据用户的问题，给出相应的天气信息。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

model = ChatTongyi(model="qwen-plus-latest", api_key=os.getenv("DASHSCOPE_API_KEY"), verbose=True)

tools = [get_weather]

agent = create_tool_calling_agent(model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": "请问你能帮我查一下今天北京的天气吗?"})
print(response["output"])
