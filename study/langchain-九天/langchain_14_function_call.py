import os

from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnableLambda
from langchain_experimental.tools import PythonAstREPLTool
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser

load_dotenv(override=True)

df = pd.read_csv("../data/WA_Fn-UseC_-Telco-Customer-Churn.xls")
# pd.set_option('max_colwidth',200)

tool = PythonAstREPLTool(locals={"df": df})
# print(tool.invoke("df['SeniorCitizen'].mean()"))
# print(df["SeniorCitizen"].mean())

system = f"""
你可以访问一个名为 `df` 的 pandas 数据框，你可以使用df.head().to_markdown() 查看数据集的基本信息， \
请根据用户提出的问题，编写 Python 代码来回答。只返回代码，不返回其他内容。只允许使用 pandas 和内置库。
"""
system_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "{input}")
])

model = ChatTongyi(model="qwen-plus-latest", api_key=os.getenv("DASHSCOPE_API_KEY"), verbose=True)

model_with_tool = model.bind_tools([tool])

parser = JsonOutputKeyToolsParser(key_name=tool.name, first_tool_only=True)

def code_print(res):
    print("code:", res["query"])
    return res

# response = model_with_tool.invoke("我有一张表，名为'df'，请帮忙计算MonthlyCharges字段的平均值")
llm_chain = system_prompt | model_with_tool | parser | RunnableLambda(code_print) | tool
print(llm_chain.invoke({"input":"我有一张表，名为'df'，请帮忙计算MonthlyCharges字段的平均值"}))