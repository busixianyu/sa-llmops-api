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


prompt = ChatPromptTemplate.from_template("{question}")

model = ChatTongyi(model="qwen-plus-latest", api_key=os.getenv("DASHSCOPE_API_KEY"), verbose=True)

model_tool = model.bind_tools([get_weather])

parser = JsonOutputKeyToolsParser(key_name=get_weather.name, first_tool_only=True)

input_chain = prompt | model_tool | parser | get_weather

output_prompt = ChatPromptTemplate.from_template(
"""你将收到一段 JSON 格式的天气数据，请用简洁自然的方式将其转述给用户。
以下是天气 JSON 数据：

```json
{weather_json}
```

请将其转换为中文天气描述，例如：
“北京当前天气晴，气温为 23°C，湿度 58%，风速 2.1 米/秒。”
只返回一句话描述，不要其他说明或解释。"""
)

output_chain = output_prompt | model | StrOutputParser()

weather_json = '{"coord": {"lon": 116.3972, "lat": 39.9075}, "weather": [{"id": 803, "main": "Clouds", "description": "\\u591a\\u4e91", "icon": "04d"}], "base": "stations", "main": {"temp": 34.94, "feels_like": 33.23, "temp_min": 34.94, "temp_max": 34.94, "pressure": 1002, "humidity": 22, "sea_level": 1002, "grnd_level": 997}, "visibility": 10000, "wind": {"speed": 6.23, "deg": 175, "gust": 9.33}, "clouds": {"all": 74}, "dt": 1749724384, "sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1749674728, "sunset": 1749728589}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}'

# result = output_chain.invoke({"weather_json": weather_json})

full_chain = input_chain | output_chain

print(full_chain.invoke({"question": "请问你能帮我查一下今天北京的天气吗?"}))
