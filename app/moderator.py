# moderator.py

import asyncio
import json
import re
from app.groq_client import call_groq
from app.characters import CHARACTERS
from app.travel_characters import TRAVEL_CHARACTERS, CITIES
from app.tts_client import speak_text

MAX_TURNS = 8  # Increased for better conversation flow


async def run_roundtable(tts_enabled=True, topic_type="government_jobs"):
    """
    Run a roundtable discussion.
    
    Args:
        tts_enabled: Enable text-to-speech
        topic_type: "government_jobs" or "travel"
    """
    if topic_type == "travel":
        return await run_travel_roundtable(tts_enabled)
    else:
        return await run_government_jobs_roundtable(tts_enabled)


async def run_government_jobs_roundtable(tts_enabled=True):
    topic = "Government Jobs and Exams in India"
    characters = CHARACTERS
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
        prompt = build_government_jobs_prompt(turns, topic, characters)

        response = await call_groq([
            {"role": "system", "content": build_government_jobs_system_prompt(characters)},
            {"role": "user", "content": prompt},
        ])

        parsed = attach_accents(parse_responses(response), characters)

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
        "topic": topic,
        "turns": turns,
    }


async def run_travel_roundtable(tts_enabled=True):
    topic = "Our Favorite Travel Destinations"
    characters = TRAVEL_CHARACTERS
    turns = []

    intro = (
        f"Welcome to the AI Roundtable Travel Edition! Today we're discussing amazing destinations: "
        f"Salt Lake City USA, Abu Dhabi UAE, Chennai and Bangalore in India, and Manchester UK. "
        f"Our panel includes Elena from Spain who's visited all these places, Fatima from UAE who's researched them extensively, "
        f"Priya from India whose sister lives abroad, and Carlos from Mexico who's planning to relocate."
    )

    turns.append({
        "speaker": "Moderator",
        "message": intro,
        "tts": None,
    })

    for turn in range(MAX_TURNS):
        prompt = build_travel_prompt(turns, topic, characters)

        response = await call_groq([
            {"role": "system", "content": build_travel_system_prompt(characters)},
            {"role": "user", "content": prompt},
        ])

        parsed = attach_accents(parse_responses(response), characters)

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
        "topic": topic,
        "turns": turns,
    }


def build_government_jobs_system_prompt(characters):
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


def build_travel_system_prompt(characters):
    char_descriptions = "\n".join([
        f"- {c['name']}: {c['role']} - {c['perspective']}"
        for c in characters
    ])
    
    return f"""
You are generating a lively, engaging roundtable discussion about travel destinations with EXACTLY 4 characters.

CHARACTERS:
{char_descriptions}

DESTINATIONS TO DISCUSS:
- Salt Lake City, USA: Mountain activities, skiing, Temple Square, craft breweries
- Abu Dhabi, UAE: Sheikh Zayed Grand Mosque, Louvre, desert safaris, luxury
- Chennai, India: Marina Beach, temples, filter coffee, seafood
- Bangalore, India: Tech hub, gardens, pub culture, pleasant weather
- Manchester, UK: Football, music scene, industrial heritage, Northern Quarter

CONVERSATION STYLE:
- Keep responses SHORT (1-3 sentences max)
- Share specific recommendations: places to visit, food to try, best seasons, activities
- Use natural, conversational language with personality
- Each character brings their unique perspective (visited, researched, sister's stories, planning to move)
- Build on what others say
- Ask follow-up questions
- Share practical tips and personal insights

OUTPUT RULES:
1. Output ONLY valid JSON
2. Output ONLY a JSON list
3. EXACTLY 4 objects with "speaker" and "message"
4. NO markdown, NO code blocks, NO trailing commas
5. Each message: 1-3 sentences maximum
"""


def build_government_jobs_prompt(turns, topic, characters):
    history = ""
    for t in turns[-6:]:
        history += f"{t['speaker']}: {t['message']}\n"

    return f"""
Topic: {topic}

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


def build_travel_prompt(turns, topic, characters):
    history = ""
    for t in turns[-6:]:
        history += f"{t['speaker']}: {t['message']}\n"

    speaker_names = [c['name'] for c in characters]
    json_template = ",\n  ".join([
        f'{{"speaker": "{name}", "message": "Short, natural travel tip/recommendation"}}'
        for name in speaker_names
    ])

    return f"""
Topic: {topic}

Recent conversation:
{history}

Now generate the NEXT TURN. Each person shares travel tips about one or more cities.

GUIDELINES:
- Keep each response 1-3 sentences
- Share specific recommendations (places, food, seasons, activities)
- Each character brings their unique perspective
- React to what others shared
- Ask follow-up questions
- Be enthusiastic and helpful

Respond with JSON list of 4 objects:

[
  {json_template}
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



def attach_accents(data, characters):
    for entry in data:
        entry.setdefault("accent", "default")
        for c in characters:
            if c["name"] == entry["speaker"]:
                entry["accent"] = c["accent"]
    return data

