from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(override=True)

model = init_chat_model("deepseek-r1:1.5b", model_provider="ollama")

question = "请介绍一下你自己"
# AIMessage
result = model.invoke(question)

print(result.content)