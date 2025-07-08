import os
import re
from typing import Literal
from datetime import datetime
from PyPDF2 import PdfReader
from models.models import TextbookSearchInput, TextbookSearchOutput

# --- PDF Setup ---

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(CURRENT_DIR, "textbook.pdf")


# --- Tool function ---

async def textbook_search_tool(input: TextbookSearchInput, request_id: str) -> TextbookSearchOutput:
    if not os.path.exists(PDF_PATH):
        return TextbookSearchOutput(
            tool_name="textbook_search",
            request_id=request_id,
            relevant_info="Textbook PDF not found.",
            timestamp=datetime.utcnow().isoformat()
        )

    reader = PdfReader(PDF_PATH)
    topic_lower = input.topic.lower()
    matches = []

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text and topic_lower in text.lower():
                match = re.search(rf".{{0,150}}{re.escape(input.topic)}.{{0,150}}", text, re.IGNORECASE)
                if match:
                    snippet = match.group(0).replace("\n", " ").strip()
                    matches.append(f"Page {i + 1}: {snippet}")
        except Exception:
            continue

        if len(matches) >= 5:
            break

    result_text = "\n\n".join(matches) if matches else "No relevant content found in textbook."

    return TextbookSearchOutput(
        tool_name="textbook_search",
        request_id=request_id,
        status="success",
        relevant_info=result_text,
        timestamp=datetime.utcnow().isoformat()
    )