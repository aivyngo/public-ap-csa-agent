import os
import re
from PyPDF2 import PdfReader
from tools.utils import make_tool

# Dynamically get the path to textbook.pdf relative to this script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(CURRENT_DIR, "textbook.pdf")

async def textbook_search(topic: str) -> str:
    if not os.path.exists(PDF_PATH):
        return "Textbook PDF not found."

    reader = PdfReader(PDF_PATH)
    topic_lower = topic.lower()
    matches = []

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text and topic_lower in text.lower():
                # Extract ~300 characters of context around the match
                match = re.search(rf".{{0,150}}{re.escape(topic)}.{{0,150}}", text, re.IGNORECASE)
                if match:
                    snippet = match.group(0).replace("\n", " ").strip()
                    matches.append(f"Page {i + 1}: {snippet}")
        except Exception:
            continue

        if len(matches) >= 5:
            break  # Limit to 5 results

    return "\n\n".join(matches) if matches else "No relevant content found in textbook."

# Register as tool
textbook_search = make_tool(
    textbook_search,
    name="textbook_search",
    description="Searches the AP CSA textbook PDF for content about a given topic.",
    param_schema={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The AP Computer Science A (Java) topic to search for in the textbook."
            }
        },
        "required": ["topic"]
    }
)
