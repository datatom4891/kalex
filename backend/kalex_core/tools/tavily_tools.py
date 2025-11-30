from langchain_core.tools import tool
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from kalex_core.prompts.tavily_prompts import tavily_search_prompt


def format_retrieved_tavily_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@tool
def tavily_search(question):
    """Uses Tavily to answer questions the LLM can't answer"""

    retriever = TavilySearchAPIRetriever(k=1)
    llm = ChatOpenAI(model="gpt-4o-mini")

    chain = (
    {"context": retriever | format_retrieved_tavily_docs, "question": RunnablePassthrough()}
    | tavily_search_prompt
    | llm
    | StrOutputParser()
    )
    response = chain.invoke(question)
    return response