import re
from langchain_core.prompts import ChatPromptTemplate

from multi_agent_crs.utils import get_action_predictor_agent_prompt, get_action_model

def action_predictor_agent(config):
    model = get_action_model(config)
    prompt = get_action_predictor_agent_prompt(config)
    prompt_template = ChatPromptTemplate.from_messages([("user", prompt)])
    planner = prompt_template | model
    return planner

def get_next_action(state):
    config = state['config']
    task = state["task"]
    planner = action_predictor_agent(config)
    result = planner.invoke({"task": task})

    # Extract the dictionary-like JSON structure
    action_list = ['recommend_item_to_user', 'ask_clarification_question', 'recommend_items', 'chit-chat', 'provide_features']
    for action in action_list:
        if action in result.content:
            return {"action_": action}
        
    return {"action_": ""}