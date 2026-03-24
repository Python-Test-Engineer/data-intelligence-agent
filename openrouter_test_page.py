from __future__ import annotations

import json
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env", override=False)

MODEL = os.environ.get("OPENROUTER_MODEL", "anthropic/claude-opus-4.1")
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api"
PROMPT = "Capital of France"


def main() -> None:
    if not API_KEY:
        print(
            json.dumps(
                {"prompt": PROMPT, "response": "OPENROUTER_API_KEY is not set in .env"},
                ensure_ascii=False,
            )
        )
        return

    try:
        client = anthropic.Anthropic(api_key=API_KEY, base_url=OPENROUTER_BASE_URL)
        response = client.messages.create(
            model=MODEL,
            max_tokens=200,
            messages=[{"role": "user", "content": PROMPT}],
        )
        text_content = next(
            (block.text for block in response.content if block.type == "text"),
            "",
        ).strip()
    except Exception as exc:
        text_content = f"ERROR: {exc}"

    print(
        json.dumps(
            {
                "prompt": PROMPT,
                "response": text_content or "<no text content returned>",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
