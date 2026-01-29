# moderator.py

import asyncio
import json
import re
from app.groq_client import call_groq
from app.characters import CHARACTERS
from app.tts_client import speak_text

TOPIC = "Government Jobs and Exams in India"
MAX_TURNS = 8  # Increased for better conversation flow


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

        parsed = attach_accents(parse_responses(response))

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
You are generating a lively, engaging roundtable discussion with EXACTLY 4 characters.

CHARACTERS:
- Exam Strategist: Experienced mentor, practical and strategic
- Serving Officer: Current government officer, realistic and grounded
- Fresh Qualifier: Recent exam qualifier, energetic and relatable
- Citizen: Informed citizen, asks tough questions, sometimes skeptical

CONVERSATION STYLE:
- Keep responses SHORT (1-3 sentences max)
- Use natural, conversational language
- Show personality and emotion
- Disagree respectfully when appropriate
- Build on what others say
- Ask follow-up questions
- Use examples and stories

OUTPUT RULES:
1. Output ONLY valid JSON
2. Output ONLY a JSON list
3. EXACTLY 4 objects with "speaker" and "message"
4. NO markdown, NO code blocks, NO trailing commas
5. Each message: 1-3 sentences maximum
"""


def build_prompt(turns):
    history = ""
    for t in turns[-6:]:
        history += f"{t['speaker']}: {t['message']}\n"

    return f"""
Topic: {TOPIC}

Recent conversation:
{history}

Now generate the NEXT TURN with natural, engaging responses.

GUIDELINES:
- Keep each response 1-3 sentences
- Show personality and emotion
- React to what others said
- Ask questions or challenge ideas when natural
- Use examples from Indian context
- Make it sound like a real conversation

Respond with JSON list of 4 objects:

[
  {{"speaker": "Exam Strategist", "message": "Short, natural response" }},
  {{"speaker": "Serving Officer", "message": "Short, natural response" }},
  {{"speaker": "Fresh Qualifier", "message": "Short, natural response" }},
  {{"speaker": "Citizen", "message": "Short, natural response" }}
]

NO extra text. NO markdown.
"""


def parse_responses(text):
    text = text.strip()

    # Case 1: Already valid JSON
    try:
        return json.loads(text)
    except:
        pass

    # Case 2: Extract JSON from inside wrappers / partial output
    start = text.find("[")
    end = text.rfind("]")
    if start != -1:
        candidate = text[start:end + 1] if end != -1 else text[start:] + "]"
        # Remove trailing commas before ] or }
        candidate = re.sub(r",\s*(\]|\})", r"\1", candidate)
        try:
            return json.loads(candidate)
        except:
            pass

    raise RuntimeError(f"Groq returned invalid JSON:\n{text}")



def attach_accents(data):
    for entry in data:
        entry.setdefault("accent", "default")
        for c in CHARACTERS:
            if c["name"] == entry["speaker"]:
                entry["accent"] = c["accent"]
    return data

