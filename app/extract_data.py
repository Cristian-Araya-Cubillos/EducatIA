from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import gradio as gr
from gradio.themes.base import Base
import params

client = MongoClient("mongodb+srv://cristianarayac2:1234321@cluster0.p8v1v.mongodb.net/")
dbName = "education"
collectionName = "education"
collection = client[dbName][collectionName]
index_name = "vectorSearch_index"

# Define the text embedding model
import os

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))

# Initialize the Vector Store

vectorStore = MongoDBAtlasVectorSearch( collection, embeddings )

def query_data(query):
    # Convert question to vector using OpenAI embeddings
    # Perform Atlas Vector Search using Langchain's vectorStore
    # similarity_search returns MongoDB documents most similar to the query    

    docs = vectorStore.similarity_search(query, K=1)
    if not docs:
        return "No se encontraron documentos, ignorar esto"
    as_output = docs[0].page_content

    # Leveraging Atlas Vector Search paired with Langchain's QARetriever

    # Define the LLM that we want to use -- note that this is the Language Generation Model and NOT an Embedding Model
    # If it's not specified (for example like in the code below),
    # then the default OpenAI model used in LangChain is OpenAI GPT-3.5-turbo, as of August 30, 2023
    
    llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'), temperature=0)


    # Get VectorStoreRetriever: Specifically, Retriever for MongoDB VectorStore.
    # Implements _get_relevant_documents which retrieves documents relevant to a query.
    retriever = vectorStore.as_retriever()
    

    # Load "stuff" documents chain. Stuff documents chain takes a list of documents,
    # inserts them all into a prompt and passes that prompt to an LLM.

    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)

    # Execute the chain

    retriever_output = qa.run(query)
    print(retriever_output)
    # Return Atlas Vector Search output, and output generated using RAG Architecture
    #return as_output, retriever_output
    return retriever_output