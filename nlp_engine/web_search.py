from duckduckgo_search import DDGS

def search_web(query):
    try:
        print(f"🌐 Assistant is searching: {query}")
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            if results:
                return results[0]['body']
            return "I couldn't find a specific answer on the web."
    except Exception as e:
        print(f"❌ Search Error: {e}")
        return "I'm having trouble connecting to my search engine."