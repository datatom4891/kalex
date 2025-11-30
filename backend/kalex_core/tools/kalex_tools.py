from kalex_core.tools.tavily_tools import tavily_search
from kalex_core.tools.memory_tools import search_user_core_memories, save_user_core_memory

kalex_tools = [save_user_core_memory, search_user_core_memories, tavily_search]