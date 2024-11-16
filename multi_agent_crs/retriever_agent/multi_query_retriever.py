from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

def csv_loader(config):
    loader = CSVLoader(file_path=config['dataset_path'], encoding='utf-8-sig')
    data = loader.load()
    return data

def multi_query_retriever_agent(config):
    docs = csv_loader(config)
    api_key = config['OPENAI_API_KEY']
    embedding = OpenAIEmbeddings(api_key=api_key)
    vectordb = Chroma.from_documents(documents=docs, embedding=embedding)
    llm = ChatOpenAI(temperature=0, api_key=api_key)
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=vectordb.as_retriever(), llm=llm
    )
    return retriever_from_llm


