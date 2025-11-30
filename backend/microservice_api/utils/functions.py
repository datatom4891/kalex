from langchain_core.messages import HumanMessage
from kalex_core.graph.graph import assemble_kalex
from microservice_api.utils.config import llm_config

kalex = assemble_kalex()

def ask_kalex(user_prompt):
    messages = [HumanMessage(content=user_prompt)]
    response = kalex.invoke({"messages": messages}, config=llm_config)
    response_from_kalex = response["messages"][-1]
    return response_from_kalex.content