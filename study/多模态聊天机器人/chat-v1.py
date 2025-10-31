from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_template = ChatPromptTemplate.from_messages([
    ('system', '你是一个多模态聊天机器人，支持文字、图片、语音、视频、文件等格式的输入和输出。'),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ('human', '{input}')
])

llm = init_chat_model(
    model='qwen3:0.6b',
    model_provider='ollama'
)

chain = prompt_template | llm | StrOutputParser()
while True:
    user_input = input("User: ")
    if not user_input:
        break
    print("AI: ", end='')
    for chunk in chain.stream({"input": user_input}):
        print(chunk, end='', flush=True)
    print()

