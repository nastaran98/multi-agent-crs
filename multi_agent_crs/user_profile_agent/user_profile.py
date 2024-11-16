from multi_agent_crs.graph import ReWOO
from multi_agent_crs.utils import get_model
from langchain_core.prompts import ChatPromptTemplate

def user_profile_agent(config):
    model = get_model(config, 'user_profile_agent')
    prompt = config['user_profile_agent']['prompt']
    prompt_template = ChatPromptTemplate.from_messages([("user", prompt)])
    user_profile_agent = prompt_template | model

    return user_profile_agent
