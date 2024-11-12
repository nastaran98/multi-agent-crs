import os
import json

from langchain_chroma import Chroma  # New import path
from langchain_core.documents import Document
import chromadb.utils.embedding_functions as embedding_functions
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings  # Updated embedding import
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.tools.retriever import create_retriever_tool
from langchain.chains.query_constructor.base import AttributeInfo

from multi_agent_crs.utils import load_data, process_data

def create_documents(config):
    docs = []
    df = load_data(config)
    for _, row in df.iterrows():
        page_content = row['title'] + row['writer'] 
        metadata = {
            "title": row['title'],
            "writer": row['writer'],
            "main_idea": row['main_idea'],
            "short_description": row['short_description'],
            "genre": row['genre'],
            "category": row['category']
        }
        doc = Document(page_content=page_content, metadata=metadata)
        docs.append(doc)
    return docs

def create_vector_store(config):
    process_data(config)
    docs = create_documents(config)
    api_key = config['OPENAI_API_KEY']
    openai_ef = OpenAIEmbeddings(api_key=api_key)
    vectorstore = Chroma.from_documents(docs, openai_ef, persist_directory="./chroma_db")
    return vectorstore

def load_vectore_store(config):
    db_path = config['db_path']
    api_key = config['OPENAI_API_KEY']
    openai_ef = OpenAIEmbeddings(api_key=api_key)
    if not os.path.exists(db_path):
        vector_store = create_vector_store(config)
    else:
        vector_store = Chroma(persist_directory="./chroma_db", embedding_function=openai_ef)
    return vector_store

def get_attribute_info():
    metadata_field_info = [
        AttributeInfo(
            name="writer",
            description="writer(author) of the book",
            type="string",
        ),
        AttributeInfo(
            name="main_idea",
            description="The main idea of book(main topic)",
            type="integer",
        ),
        AttributeInfo(
            name="short_description",
            description="short description about book",
            type="integer",
        ),
        AttributeInfo(
            name="genre",
            description="short description about book. it can be one of One of ['فلسفه','عاشقانه','کارآگاهی','کمدی','وحشت']",
            type="integer",
        ),
        AttributeInfo(
            name="category",
            description="category of book. it can be one of One of ['داستانی','غیر داستانی','رمان','تاریخ']",
            type="integer"
        )
    ]
    return metadata_field_info

# def query_constructor(config, attribute_info):
#     doc_contents = config['doc_contents']
#     prompt = get_query_constructor_prompt(doc_contents, attribute_info)
#     prompt = prompt.format(query="{query}")
#     return prompt

def create_retriever(config, vector_store, attribute_info):
    doc_contents = config['doc_contents']
    api_key = config['OPENAI_API_KEY']
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

    retriever = SelfQueryRetriever.from_llm(
        llm,
        vector_store,
        doc_contents,
        attribute_info,
    )
    return retriever

def retrieve_items(query, retriever):
    docs = retriever.invoke({"query": query})
    return docs

def retriever_tool(config):
    vector_store = load_vectore_store(config)
    attribute_info = get_attribute_info()
    retriever = create_retriever(config, vector_store, attribute_info)
    retriever_tool = create_retriever_tool(
        retriever,
        "Retriever",
        "Search and retrieve items from database.",
    )
    return retriever_tool
