# api_oai.py - OpenAI API (plain text, no structured output)

import os
import sys
import time

from openai import OpenAI

MODEL_NAME = "gpt-5.5"

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENROUTER_API_KEY or OPENAI_API_KEY environment variable not set.")
            sys.exit(1)

        if os.getenv("OPENROUTER_API_KEY"):
            _client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        else:
            _client = OpenAI(api_key=api_key)
    return _client


def call_llm(system_prompt, user_prompt, temperature=1.0, web_search=True,
             reasoning_effort="xhigh"):
    """Call OpenAI (streaming) and return plain text response.

    Args:
        reasoning_effort: none, low, medium, high, xhigh
    """
    input_text = f"{system_prompt}\n\n{user_prompt}" if system_prompt else user_prompt

    max_retries = 3
    for attempt in range(max_retries):
        try:
            kwargs = {
                "model": MODEL_NAME,
                "input": [{"role": "user", "content": input_text}],
                "temperature": temperature,
                "stream": True,
            }
            if reasoning_effort != "none":
                kwargs["reasoning"] = {"effort": reasoning_effort}
            if web_search:
                kwargs["tools"] = [{"type": "web_search_preview"}]

            stream = get_client().responses.create(**kwargs)
            final_response = None
            for event in stream:
                if event.type == "response.output_text.delta":
                    print(getattr(event, "delta", ""), end="", flush=True, file=sys.stderr)
                elif event.type == "response.completed":
                    print("", file=sys.stderr)
                    final_response = event.response
                elif event.type in ("response.failed", "response.incomplete"):
                    print(f"Stream failed with status: {event.type}")
                    return None
            if final_response is None:
                print("Stream ended without response.completed event")
                return None

            for item in final_response.output:
                if item.type == "message":
                    return item.content[0].text
            return final_response.output[-1].content[0].text
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"API call failed: {e}. Retrying in 5s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
            else:
                print(f"API call failed after {max_retries} retries: {e}")
                return None
