from multi_agent_crs.utils import get_model
from langchain_core.prompts import ChatPromptTemplate

def ask_clarification(config):
    model = get_model(config, 'ask_clarification')
    prompt = config['ask_clarification']['prompt']
    prompt_template = ChatPromptTemplate.from_messages([("user", prompt)])
    ask_clarification = prompt_template | model
    return ask_clarification