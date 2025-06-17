import httpx
from tools.utils import make_tool

SERPER_API_KEY = "7ca1e00336f1944166687f9a5a9cc316f8533f6a"

async def web_search(topic: str) -> str:
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {"q": f" AP Computer Science: {topic}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        data = response.json()

        results = data.get("organic", [])
        output = "\n".join(f"- {r['title']}: {r['link']}" for r in results[:5])
        return output or "No relevant search results found."

web_search = make_tool(
    web_search,
    name="web_search",
    description="Searches for AP CSA and Java information on the web.",
    param_schema={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The AP Computer Science A (Java) topic to search online for."
            }
        },
        "required": ["topic"]
    }
)