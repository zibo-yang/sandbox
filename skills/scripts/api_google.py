# api_google.py - Google Gemini API (plain text, no structured output)

import os
import sys
import time

from google import genai
from google.genai.types import Tool, GoogleSearch

MODEL_NAME = "gemini-3.1-pro-preview"

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not set.")
            sys.exit(1)
        _client = genai.Client(api_key=api_key)
    return _client


def call_llm(system_prompt, user_prompt, model=None, temperature=1.0, web_search=True):
    """Call Gemini and return plain text response."""
    config = {"temperature": temperature, "system_instruction": system_prompt}
    if web_search:
        config["tools"] = [Tool(google_search=GoogleSearch())]

    contents = [{"role": "user", "parts": [{"text": user_prompt}]}]

    max_retries = 3
    for attempt in range(max_retries):
        try:
            chunks = []
            for chunk in get_client().models.generate_content_stream(
                model=model or MODEL_NAME,
                contents=contents,
                config=config,
            ):
                if chunk.text:
                    chunks.append(chunk.text)
                    print(chunk.text, end="", flush=True, file=sys.stderr)
            if chunks:
                print("", file=sys.stderr)
                return "".join(chunks)
            return None
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"API call failed: {e}. Retrying in 5s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
            else:
                print(f"API call failed after {max_retries} retries: {e}")
                return None
