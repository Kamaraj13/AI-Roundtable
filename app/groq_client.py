# groq_client.py

import os
import httpx

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"


async def call_groq(messages):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.8,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        res = await client.post(GROQ_URL, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()

    return data["choices"][0]["message"]["content"]

