
from multi_agent_crs.graph import ReWOO
from multi_agent_crs.utils import get_solver_model

def solve(state: ReWOO):
    config = state['config']
    solve_prompt = config['solver_agent']['prompt']
    model = get_solver_model(config)

    plan = ""
    for _plan, step_name, tool, tool_input in state["steps"]:
        _results = (state["results"] or {}) if "results" in state else {}
        for k, v in _results.items():
            tool_input = tool_input.replace(k, v)
            step_name = step_name.replace(k, v)
        plan += f"Plan: {_plan}\n{step_name} = {tool}[{tool_input}]"
    prompt = solve_prompt.format(plan=plan, task=state["task"], action_= state["action_"])
    result = model.invoke(prompt)
    return {"result": result.content}