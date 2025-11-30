import os
import tiktoken
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import get_buffer_string
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END

from kalex_core.tools.kalex_tools import kalex_tools
from kalex_core.tools.memory_tools import search_user_core_memories
from kalex_core.states import State
from kalex_core.structured_output.vagueness_validation import IsQuestionVague
from kalex_core.prompts.kalex_system_prompts import sys_prompt
from kalex_core.prompts.question_vagueness_prompts import vagueness_prompt_template

load_dotenv(dotenv_path=".env", override=True)

model = ChatOpenAI(model_name="gpt-4o-mini")
model_with_tools = model.bind_tools(kalex_tools)

tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")

def agent(state: State) -> State:
    """Process the current state and generate a response using the LLM.

    Args:
        state (schemas.State): The current state of the conversation.

    Returns:
        schemas.State: The updated state with the agent's response.
    """
    chain = sys_prompt | model_with_tools
    recall_str = (
        "<recall_memory>\n" + "\n".join(state["recall_memories"]) + "\n</recall_memory>"
    )
    response = chain.invoke(
        {
            "messages": state["messages"],
            "recall_memories": recall_str,
        }
    )
    return {"messages": [response]}

def load_memories(state: State, config: RunnableConfig) -> State:
    """Load memories for the current conversation.

    Args:
        state (schemas.State): The current state of the conversation.
        config (RunnableConfig): The runtime configuration for the agent.

    Returns:
        State: The updated state with loaded memories.
    """
    convo_str = get_buffer_string(state["messages"])
    convo_str = tokenizer.decode(tokenizer.encode(convo_str)[:2048])
    recall_memories = search_user_core_memories.invoke(convo_str, config)
    return {"recall_memories": recall_memories,}

def route_tools(state: State):
    """Determine whether to use tools or end the conversation based on the last message.

    Args:
        state (schemas.State): The current state of the conversation.

    Returns:
        Literal["tools", "__end__"]: The next step in the graph.
    """
    msg = state["messages"][-1]
    if msg.tool_calls:
        return "tools"

    return END