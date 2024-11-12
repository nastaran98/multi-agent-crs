import re
from langchain_core.prompts import ChatPromptTemplate

from multi_agent_crs.utils import get_planner_prompt, get_planner_model
from multi_agent_crs.graph import ReWOO

def planner_agent(config):
    model = get_planner_model(config)
    prompt = get_planner_prompt(config)
    prompt_template = ChatPromptTemplate.from_messages([("user", prompt)])
    planner = prompt_template | model
    return planner

pattern = re.compile(r"Plan\s*\d*:\s*(.+?)\s*\n\s*-\s*(#E\d+)\s*=\s*(\w+)\[([^\]]+)\]", re.DOTALL)

# Replacement function to format the steps to match the desired regex pattern
def reformat_step(match):
    description = match.group(1).strip()
    identifier = match.group(2)
    tool = match.group(3)
    tool_input = match.group(4)
    return f"Plan: {description} {identifier} = {tool} [{tool_input}]"

def get_plan(state):
    config = state['config']
    regex_pattern = r"Plan\s*\d*:\s*(.+?)\s*#(E\d+)\s*=\s*(\w+)\[([^\]]+)\]"
    task = state["task"]
    action = state["action_"]
    planner = planner_agent(config)
    result = planner.invoke({"task": task, "action_": action})
    # formatted_plan_string = pattern.sub(reformat_step, result.content)
    matches = re.findall(regex_pattern, result.content)
    return {"steps": matches, "plan_string": result.content}