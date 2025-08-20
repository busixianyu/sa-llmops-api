import uuid
from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, Any

from dotenv import load_dotenv
from injector import inject
from langchain.chat_models import init_chat_model
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.tracers import Run
from internal.core.tool.builtin_tool.provider import ProviderFactory
from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message

load_dotenv()


@inject
@dataclass
class AppHandler:

    app_service: AppService
    provider_factory: ProviderFactory

    def ping(self):
        providers = self.provider_factory.get_provider_entities()
        return success_json(data={"providers": [provider.model_dump() for provider in providers]})
        # raise FailException("数据未找到")

    @staticmethod
    def _load_memory_variables(input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        configurable = config.get("configurable", {})
        config_memory = configurable.get("memory", None)
        if config_memory is not None and isinstance(config_memory, BaseMemory):
            return config_memory.load_memory_variables(input)
        return {
            "history": []
        }

    @staticmethod
    def _save_context(run_obj: Run, config: RunnableConfig):
        configurable = config.get("configurable", {})
        config_memory = configurable.get("memory", None)
        if config_memory is not None and isinstance(config_memory, BaseMemory):
            config_memory.save_context(run_obj.inputs, run_obj.outputs)

    def debug(self, app_id: uuid.UUID):
        """聊天接口"""
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # query = request.json.get("query")

        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个强大的聊天机器人，能根据用户的提问回答对应的问题"),
            MessagesPlaceholder("history"),
            ("human", "{query}")
        ])

        memory = ConversationBufferWindowMemory(
            k=3,
            input_key="query",
            output_key="output",
            return_messages=True,
            chat_memory=FileChatMessageHistory(f"./storage/memory/{app_id}.txt")
        )

        llm = init_chat_model(model="qwen3:latest", model_provider="ollama")

        # llm = ChatOpenAI(
        #     model=os.getenv("DASHSCOPE_MODEL"),
        #     api_key=os.getenv("DASHSCOPE_API_KEY"),
        #     base_url=os.getenv("DASHSCOPE_API_URL")
        # )

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
        chain = (RunnablePassthrough.assign(
            history=RunnableLambda(self._load_memory_variables) | itemgetter('history')
        ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)
        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input, config={"configurable": {"memory": memory}})
        # memory.save_context(chain_input, {"output": content})
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