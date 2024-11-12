from multi_agent_crs.graph import ReWOO
from multi_agent_crs.utils import get_model
from langchain_core.prompts import ChatPromptTemplate

def answer_generator(state: ReWOO):
    config = state['config']
    task = state['task']
    action = state['action_']
    model = get_model(config, 'answer_generator')
    prompt = config['answer_generator']['prompt']
    prompt_template = ChatPromptTemplate.from_messages([("user", prompt)])
    answer_generator = prompt_template | model
    result = answer_generator.invoke({'task': task, 'action': action})

    return {"result": result.content}