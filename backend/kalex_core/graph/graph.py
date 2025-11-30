from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from kalex_core.states import State
from kalex_core.graph.kalex_nodes import *
from kalex_core.tools.kalex_tools import kalex_tools

def assemble_kalex():
    # Create the graph and add nodes
    builder = StateGraph(State)
    builder.add_node(load_memories)
    builder.add_node(agent)
    builder.add_node("tools", ToolNode(kalex_tools))

    # Add edges to the graph
    builder.add_edge(START, "load_memories")
    builder.add_edge("load_memories", "agent")
    builder.add_conditional_edges("agent", route_tools, ["tools", END])
    builder.add_edge("tools", "agent")

    # Compile the graph
    memory = MemorySaver()
    kalex = builder.compile(checkpointer=memory)

    return kalex