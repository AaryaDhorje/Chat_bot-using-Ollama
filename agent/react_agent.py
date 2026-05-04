from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from config import MODEL_NAME, TEMPERATURE, RECURSION_LIMIT
from tools.search import get_tools
from prompts.system_prompt import SYSTEM_PROMPT


def build_agent():
    llm = ChatOllama(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    tools = get_tools()

    agent = create_react_agent(llm, tools).with_config({
        "recursion_limit": RECURSION_LIMIT,
        "system_message": SYSTEM_PROMPT,
    })

    return agent