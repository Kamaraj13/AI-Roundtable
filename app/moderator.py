# moderator.py

import asyncio
import json
import re
from app.groq_client import call_groq
from app.characters import CHARACTERS
from app.tts_client import speak_text

TOPIC = "Government Jobs and Exams in India"
MAX_TURNS = 6  # free-tier friendly


async def run_roundtable(tts_enabled=True):
    turns = []

    intro = (
        "Welcome to the AI Roundtable. Today we discuss Government Jobs and Exams in India. "
        "Our panel includes an Exam Strategist, a Serving Officer, a Fresh Qualifier, and a Citizen."
    )

    turns.append({
        "speaker": "Moderator",
        "message": intro,
        "tts": None,
    })

    for turn in range(MAX_TURNS):
        prompt = build_prompt(turns)

        response = await call_groq([
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": prompt},
        ])

        parsed = parse_responses(response)

        for entry in parsed:
            tts_file = None
            if tts_enabled:
                tts_file = await speak_text(entry["message"], entry["accent"])

            turns.append({
                "speaker": entry["speaker"],
                "message": entry["message"],
                "tts": tts_file,
            })

        await asyncio.sleep(0.3)

    return {
        "topic": TOPIC,
        "turns": turns,
    }


def build_system_prompt():
    return """
You are an AI generating a roundtable with EXACTLY 4 characters.

YOUR OUTPUT MUST FOLLOW THESE RULES:

1. Output ONLY valid JSON.
2. Output ONLY a JSON list. No text before or after.
3. The list must contain EXACTLY 4 objects.
4. Each object must have:
   - "speaker": one of the 4 character names
   - "message": the character's spoken response
5. DO NOT add commentary, markdown, or explanations.
6. DO NOT wrap the JSON in ```json or any code block.
7. DO NOT include trailing commas.

If you break JSON format, the system will fail.
"""


def build_prompt(turns):
    history = ""
    for t in turns[-6:]:
        history += f"{t['speaker']}: {t['message']}\n"

    return f"""
Topic: {TOPIC}

Recent conversation:
{history}

Now generate the NEXT TURN.

Respond ONLY with a JSON list of 4 objects, like this:

[
  {{"speaker": "Exam Strategist", "message": "..." }},
  {{"speaker": "Serving Officer", "message": "..." }},
  {{"speaker": "Fresh Qualifier", "message": "..." }},
  {{"speaker": "Citizen", "message": "..." }}
]

NO extra text. NO markdown. NO commentary.
"""


def parse_responses(text):
    # Try direct JSON
    try:
        return attach_accents(json.loads(text))
    except:
        pass

    # Try extracting JSON list using regex
    try:
        json_str = re.search(r"`\(⁠.*\)`", text, re.DOTALL).group(0)
        return attach_accents(json.loads(json_str))
    except:
        raise RuntimeError(f"Groq returned invalid JSON:\n{text}")


def attach_accents(data):
    for entry in data:
        for c in CHARACTERS:
            if c["name"] == entry["speaker"]:
                entry["accent"] = c["accent"]
    return data

