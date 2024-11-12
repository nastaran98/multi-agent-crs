from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
import os

from multi_agent_crs.utils import get_model
def create_sql(df):
    engine = create_engine("sqlite:///books.db")
    df.to_sql("books", engine, index=False)
    db = SQLDatabase(engine=engine)
    return db

def query_database_agent(df, config):
    db = create_sql(df)
    llm = get_model(config, 'sql_query_agent')
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    return agent_executor

