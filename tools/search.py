from langchain_community.tools import DuckDuckGoSearchRun


def get_tools():
    search_tool = DuckDuckGoSearchRun()
    return [search_tool]