import os
import uuid

from internal.schema.app_schema import CompletionReq
from dotenv import load_dotenv
from flask import request
from openai import OpenAI
from pkg.response import success_json, validate_error_json, success_message
from internal.exception import FailException
from internal.service import AppService
from injector import inject
from dataclasses import dataclass
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


load_dotenv()


@inject
@dataclass
class AppHandler:

    app_service: AppService

    def ping(self):
        raise FailException("数据未找到")

    def debug(self, app_id: uuid.UUID):
        """聊天接口"""
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # query = request.json.get("query")

        prompt = ChatPromptTemplate.from_template("{query}")

        llm = ChatOpenAI(
            model=os.getenv("DASHSCOPE_MODEL"),
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url=os.getenv("DASHSCOPE_API_URL")
        )

        # client = OpenAI(
        #     api_key=os.getenv("DASHSCOPE_API_KEY"),
        #     base_url=os.getenv("DASHSCOPE_API_URL")
        # )
        # completion = client.chat.completions.create(
        #     model=os.getenv("DASHSCOPE_MODEL"),
        #     messages=[
        #         {"role": "system",
        #          "content": "你是一个乐于助人的智能助手，你的名字叫小帅，请根据用户的输入和上下文回答问题"},
        #         {"role": "user", "content": req.query.data}
        #     ]
        # )

        # ai_message = llm.invoke(prompt.invoke({"query": req.query.data}))
        #
        # parser = StrOutputParser()
        #
        # content = parser.invoke(ai_message)
        chain = prompt | llm | StrOutputParser()
        content = chain.invoke({"query": req.query.data})

        # content = completion.choices[0].message.content
        return success_json(content)

    def create_app(self):
        """调用服务创建新的app记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已经成功创建，id:{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"get app id:{app.id}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功更新，id:{app.id}, name:{app.name}")

    def delete_app(self, id: uuid.UUID):
        self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，id:{id}")