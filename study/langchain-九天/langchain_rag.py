from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

chat = ChatZhipuAI(
    model="glm-4"
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)