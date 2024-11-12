from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.query_constructors.chroma import ChromaTranslator
from langchain.tools.retriever import create_retriever_tool
from langchain.chains.query_constructor.base import AttributeInfo, get_query_constructor_prompt, StructuredQueryOutputParser

import os

from langchain_chroma import Chroma  # New import path
from langchain_core.documents import Document
import chromadb.utils.embedding_functions as embedding_functions
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings  # Updated embedding import

from multi_agent_crs.utils import load_data, process_data

def create_page_content(row):
    page_content = 'کتاب {title} توسط {writer} نوشته شده است. ایده اصلی این کتاب {main_idea} است و این کتاب در ژانر {genre} نوشته شده و در دسته‌بندی {category} قرار می‌گیرد.'
    page_content = page_content.format(
        title= row['title'],
        writer= row['writer'],
        main_idea= row['main_idea'],
        short_description= row['short_description'],
        genre= row['genre'],
        category= row['category']
    )
    return page_content
def create_documents(config):
    docs = []
    df = load_data(config)
    for _, row in df.iterrows():
        page_content = create_page_content(row)
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


def create_retriever(config):
    document_content_description = "book title along with writer's name"

    # Define allowed comparators list
    allowed_comparators = [
        "$eq",  # Equal to (number, string, boolean)
        "$ne",  # Not equal to (number, string, boolean)
        "$gt",  # Greater than (number)
        "$gte",  # Greater than or equal to (number)
        "$lt",  # Less than (number)
        "$lte",  # Less than or equal to (number)
    ]

    examples = [
        (
            "یه کتاب از خالد حسینی میخوام بخونم.",
            {
                "query": "کتاب از خالد حسینی",
                "filter": 'eq("writer", ["خالد حسینی]")',
            },
        ),
        (
            "یه کتاب کارآگاهی میخوام بخونم",
            {
                "query": "کتاب کارآگاهی",
                "filter": 'or(eq("genre", "کارآگاهی"), eq("short_description", "کارآگاهی"))',
            },
        ),
        (
            "یه کتاب درباره اقتصاد بهم پیشنهاد بده",
            {
                "query": "کتاب درباره اقتصاد",
                "filter": 'or(eq("genre", "اقتصاد"), eq("short_description", "اقتصاد"))',
            },
        )
    ]

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

    constructor_prompt = get_query_constructor_prompt(
        document_content_description.encode('utf-8').decode('utf-8'),
        metadata_field_info,
        allowed_comparators=allowed_comparators,
        examples=examples,
    )

    output_parser = StructuredQueryOutputParser.from_components()
    api_key = config['OPENAI_API_KEY']
    llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
    query_constructor = constructor_prompt | llm | output_parser

    vector_store = load_vectore_store(config)
    retriever = SelfQueryRetriever(
        query_constructor=query_constructor,
        vectorstore=vector_store,
        structured_query_translator=ChromaTranslator(),
        search_kwargs={'k': 5}
    )
    return retriever

def retriever_tool_(config):
    retriever = create_retriever(config)
    retriever_tool = create_retriever_tool(
        retriever,
        "Retriever",
        "Search and retrieve items from database.",
    )
    return retriever_tool
