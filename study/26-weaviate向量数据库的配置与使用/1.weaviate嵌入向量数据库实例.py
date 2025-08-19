from dotenv import load_dotenv
import weaviate
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.classes.query import Filter


load_dotenv()

# 随机生成一些中文文档信息
text = [
    "这是一个测试文本，用于测试文本向量化。",
    "这是另一个测试文本，用于测试文本向量化。",
    "笨笨是一只爱睡觉的猫咪",
    "学习新技能是每个人都应该追求的目标",
    "我的手机突然关机了，让我很焦虑",
    "我喜欢吃苹果和香蕉，但是不喜欢吃梨子",
    "我喜欢看电影，但不是特别喜欢看恐怖片",
    "我喜欢听音乐，尤其是在周末的时候",
    "我的狗喜欢追逐球，看起来非常开心"
]

metadatas = [
    {"page": 1},
    {"page": 2},
    {"page": 3},
    {"page": 4},
    {"page": 5},
    {"page": 6, "account_id": 1},
    {"page": 7},
    {"page": 8},
    {"page": 9}
]

with weaviate.connect_to_local("localhost", 8080) as client:

    embeddings = OllamaEmbeddings(model="bge-m3:567m")

    db = WeaviateVectorStore(client=client, embedding=embeddings, index_name="DatasetTest", text_key="text")
    # db.add_texts(text, metadata=metadatas)
    # filters = Filter.by_property("page").greater_or_equal(2)
    # print(db.similarity_search_with_score("笨笨", k=4, filters=filters))
    # db.delete(ids=["DatasetTest"])
    retriever = db.as_retriever()
    print(retriever.invoke("笨笨"))