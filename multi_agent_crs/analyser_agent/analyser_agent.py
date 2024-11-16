from multi_agent_crs.graph import ReWOO
from multi_agent_crs.utils import get_model
from langchain_core.prompts import ChatPromptTemplate

def analyser_agent(config):
    model = get_model(config, 'LLM_agent')
    prompt = config['LLM_agent']['prompt']
    prompt_template = ChatPromptTemplate.from_messages([("user", prompt)])
    analyser_agent = prompt_template | model

    return analyser_agent
