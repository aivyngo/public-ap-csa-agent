import httpx
from typing import Literal
from datetime import datetime
from models.models import WebSearchInput, WebSearchOutput

SERPER_API_KEY = "7ca1e00336f1944166687f9a5a9cc316f8533f6a"

# --- Tool function ---

async def web_search(input: WebSearchInput, request_id: str) -> WebSearchOutput:
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {"q": f"AP Computer Science: {input.topic}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        data = response.json()

    results = data.get("organic", [])
    output = "\n".join(f"- {r['title']}: {r['link']}" for r in results[:5])

    if not output:
        output = "No relevant search results found."

    return WebSearchOutput(
        tool_name="web_search",
        request_id=request_id,
        status="success",
        relevant_info=output,
        timestamp=datetime.utcnow().isoformat()
    )
