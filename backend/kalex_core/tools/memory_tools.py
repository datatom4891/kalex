import uuid

from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from typing import List

from kalex_core.vector_store import longterm_memory_vs

def get_user_id(config: RunnableConfig) -> str:
    user_id = config["configurable"].get("user_id")
    if user_id is None:
        raise ValueError("User ID needs to be provided to save a memory.")

    return user_id

@tool
def save_user_core_memory(memory: str, config: RunnableConfig) -> str:
    """Save memory to vectorstore for later semantic retrieval."""
    user_id = get_user_id(config)
    document = Document(page_content=memory, id=str(uuid.uuid4()), metadata={"user_id": user_id})
    longterm_memory_vs.add_documents([document])
    return memory

@tool
def search_user_core_memories(query:str, config: RunnableConfig) -> List[str]:
    """Search for relevant memories."""
    
    user_id = get_user_id(config)
    documents = longterm_memory_vs.similarity_search(query, k=3, filter = {"user_id": user_id})
    return [document.page_content for document in documents]
