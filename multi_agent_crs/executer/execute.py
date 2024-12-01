from multi_agent_crs.graph import ReWOO
from multi_agent_crs.retriever_agent import multi_query_retriever_agent
from multi_agent_crs.query_databse import query_database_agent
from multi_agent_crs.search_agent import create_search_agent
from multi_agent_crs.analyser_agent import analyser_agent
from multi_agent_crs.answer_generator import answer_generator
from multi_agent_crs.user_profile_agent import user_profile_agent
from multi_agent_crs.ask_clarification import ask_clarification

def get_current_task(state: ReWOO):
    if "results" not in state or state["results"] is None:
        return 1
    if len(state["results"]) == len(state["steps"]):
        return None
    if 'wrong tool' in str(state['results']):
        return "error"
    else:
        return len(state["results"]) + 1

def tool_execution(state: ReWOO):
    config = state['config']
    """Worker node that executes the tools of a given plan."""
    _step = get_current_task(state)
    _, step_name, tool, tool_input = state["steps"][_step - 1]
    task = state['task']
    profile = state['profile']
    result = None
    _results = (state["results"] or {}) if "results" in state else {}
    for k, v in _results.items():
        tool_input = tool_input.replace(k, v)
    if tool == "retriever":
        tool = multi_query_retriever_agent(config)
        result = tool.invoke({"query": tool_input})
    elif tool == "LLM":
        tool = analyser_agent(config)
        result = tool.invoke({'task': task, 'tool_input': tool_input})
    elif tool == "query_db":
        tool = query_database_agent(config)
        result = tool.invoke({"input": tool_input})
    elif tool == "search":
        tool = create_search_agent(config)
        result = tool.search({"query": tool_input})
    elif tool == "answer_generator":
        tool = answer_generator(config)
        result = tool.invoke({"tool_input": tool_input, 'task': task})
    elif tool == "ask_clarification":
        tool = ask_clarification(config)
        result = tool.invoke({"tool_input": tool_input, 'task': task})
    elif tool == "user_profile":
        tool = user_profile_agent(config)
        profile = tool.invoke({"tool_input": tool_input, 'user_profile': profile})
    else:
        return {"results": f'wrong tool {tool}'}
    if result:
        _results[step_name] = str(result)
    else:
        _results[step_name] = str(profile)
    return {"results": _results}