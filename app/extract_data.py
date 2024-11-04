from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
import gradio as gr
from gradio.themes.base import Base
import params

client = MongoClient("mongodb+srv://cristianarayac2:1234321@cluster0.p8v1v.mongodb.net/")
dbName = "education"
collectionName = "materias"
collection = client[dbName][collectionName]
index_name = "vector_index"

# Define the text embedding model
import os
import time
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))

# Initialize the Vector Store

vectorStore = MongoDBAtlasVectorSearch( collection, embeddings )

def query_data(query):
    # Realizar búsqueda de similitud
    docs = vectorStore.similarity_search(query, K=1)
    print("Retrieved documents:", docs)
    time.sleep(1)
    llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), temperature=0)
    retriever = vectorStore.as_retriever()
    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
    retriever_output = qa.invoke(query)
    # Return Atlas Vector Search output, and output generated using RAG Architecture
    return retriever_output["result"]
