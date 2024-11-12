from langgraph.graph import END, StateGraph, START
from multi_agent_crs.executer import get_current_task
from .graph_state import ReWOO
from multi_agent_crs.planner_agent import get_plan
from multi_agent_crs.action_predictor_agent import get_next_action
from multi_agent_crs.executer import tool_execution
from multi_agent_crs.solver import solve
from multi_agent_crs.answer_generator import answer_generator

def tool_route(state):
    _step = get_current_task(state)
    if _step is None:
        # We have executed all tasks
        return "solve"
    if _step == "error":
        return END
    else:
        # We are still executing tasks, loop back to the "tool" node
        return "tool"

def action_route(state):
    action = state['action_']
    if 'ask_clarification_question' in str(action) or 'chit-chat' in str(action):
        # We have executed all tasks
        return "answer_generator"
    else:
        # We are still executing tasks, loop back to the "tool" node
        return "plan"    

def plan_route(state):
    if len(state['steps']) == 0:
        return END
    else:
        # We are still executing tasks, loop back to the "tool" node
        return "tool"

def create_graph():
    graph = StateGraph(ReWOO)
    graph.add_node("action", get_next_action)
    graph.add_node("plan", get_plan)
    graph.add_node("tool", tool_execution)
    graph.add_node("solve", solve)
    graph.add_node("answer_generator", answer_generator)
    graph.add_conditional_edges("plan", plan_route)
    graph.add_conditional_edges("action", action_route)
    graph.add_conditional_edges("tool", tool_route)
    graph.add_edge(START, "action")
    graph.add_edge("solve", END)
    graph.add_edge("answer_generator", END)
    app = graph.compile()
    return app