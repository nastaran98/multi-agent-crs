from multi_agent_crs.graph import ReWOO
from multi_agent_crs.utils import get_model
from langchain_core.prompts import ChatPromptTemplate

def answer_generator(config):
    model = get_model(config, 'answer_generator')
    prompt = config['answer_generator']['prompt']
    prompt_template = ChatPromptTemplate.from_messages([("user", prompt)])
    answer_generator = prompt_template | model
    return answer_generator