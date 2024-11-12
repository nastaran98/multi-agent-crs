from tavily import TavilyClient

def create_search_agent(config):
    api_key = config["TAVILY_API_KEY"]
    tavily_client = TavilyClient(api_key=api_key)
    return tavily_client
