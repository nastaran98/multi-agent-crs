from multi_agent_crs.graph import ReWOO
from multi_agent_crs.utils import get_model
from langchain_core.prompts import ChatPromptTemplate

def ranker_agent(config):
    model = get_model(config, 'ranker_agent')
    prompt = config['ranker_agent']['prompt']
    prompt_template = ChatPromptTemplate.from_messages([("user", prompt)])
    ranker_agent = prompt_template | model

    return ranker_agent
