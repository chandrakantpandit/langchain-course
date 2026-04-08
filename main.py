import os

import httpx
import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

load_dotenv()

insecure_http_client = httpx.Client(verify=False)

# Tavily uses requests.Session internally; configure proxy + SSL here.
proxy_url = os.getenv("PROXY_URL")
tavily_session = requests.Session()
tavily_session.proxies.update({"http": proxy_url, "https": proxy_url})
tavily_session.verify = False
tavily_client = TavilyClient(session=tavily_session)


@tool
def search(query: str) -> str:
    """Search the web for the query

    Args:
        query (str): The query to search for

    Returns:
        str: The search results
    """
    print(f"Searching for {query}")
    result = tavily_client.search(query, include_answer=True, max_results=3)
    answer = result.get("answer")
    if answer:
        return answer
    results = result.get("results", [])
    if results:
        top = results[0]
        return top.get("content") or top.get("title") or "No useful result content."
    return "No results returned from Tavily."


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, http_client=insecure_http_client)
agent = create_agent(model=llm, tools=[search])

messages = [
    SystemMessage(
        content="You must always call the `search` tool exactly once before answering. Use only the tool result in your final answer."
    ),
    HumanMessage(content="What is the weather in Roorkee?"),
]
response = agent.invoke({"messages": messages})
final_answer = response["messages"][-1].content
print(final_answer)


def main():
    print("Hello from langchain-course!")


if __name__ == "__main__":
    main()
