# https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/mongodb_atlas

#from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
import params
from langchain.document_loaders import DirectoryLoader
import os
# Step 1: Load
#loaders = [
 #WebBaseLoader("https://en.wikipedia.org/wiki/AT%26T"),
 #PyPDFLoader("datosA.pdf"),
 #PyPDFLoader("crisishidrica_removed.pdf")
 #WebBaseLoader("https://en.wikipedia.org/wiki/Bank_of_America")
#]

client = MongoClient("mongodb+srv://cristianarayac2:1234321@cluster0.p8v1v.mongodb.net/")
dbName = "education"
collectionName = "materias"
collection = client[dbName][collectionName]
loaders = DirectoryLoader('data', glob="./*.pdf", loader_cls=PyPDFLoader)
papers = loaders.load()
# Step 2: Transform (Split)
text_splitter = RecursiveCharacterTextSplitter (chunk_size=1000, chunk_overlap=5)
docs = text_splitter.split_documents(papers)
data = []
print('Split into ' + str(len(docs)) + ' docs')

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
vectorStore = MongoDBAtlasVectorSearch.from_documents( docs, embeddings, collection=collection )
