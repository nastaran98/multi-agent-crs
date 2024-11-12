from multi_agent_crs.graph import ReWOO
from multi_agent_crs.retriever_agent import retriever_tool_
from multi_agent_crs.ranker_agent import ranker_agent
from multi_agent_crs.query_databse import query_database_agent
from multi_agent_crs.search_agent import create_search_agent

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
    _results = (state["results"] or {}) if "results" in state else {}
    for k, v in _results.items():
        tool_input = tool_input.replace(k, v)
    if tool == "Retriever":
        tool = retriever_tool_(config)
        result = tool.invoke({"query": tool_input})
    elif tool == "Ranker":
        tool = ranker_agent(config)
        result = tool.invoke(tool_input)
    elif tool == "query_db":
        tool = query_database_agent(config)
        tool.invoke({"input": tool_input})
    elif tool == "search":
        tool = create_search_agent(config)
        tool.invoke({"query": tool_input})
    else:
        return {"results": f'wrong tool {tool}'}
    _results[step_name] = str(result)
    return {"results": _results}