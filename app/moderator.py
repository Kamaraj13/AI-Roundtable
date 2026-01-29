# moderator.py

import asyncio
import json
import re
from app.groq_client import call_groq
from app.characters import CHARACTERS
from app.travel_characters import TRAVEL_CHARACTERS, CITIES
from app.tech_startup_characters import TECH_STARTUP_CHARACTERS
from app.personal_finance_characters import PERSONAL_FINANCE_CHARACTERS
from app.mental_health_characters import MENTAL_HEALTH_CHARACTERS
from app.tts_client import speak_text

MAX_TURNS = 5  # Reduced for 2.5x faster generation while maintaining quality


async def generate_tts_batch(entries, tts_enabled):
    """Parallelize TTS generation for multiple speakers at once."""
    if not tts_enabled:
        return entries
    
    # Generate all TTS files in parallel
    tts_tasks = []
    for entry in entries:
        task = speak_text(entry["message"], entry["accent"])
        tts_tasks.append(task)
    
    tts_results = await asyncio.gather(*tts_tasks, return_exceptions=True)
    
    # Attach results to entries
    for entry, tts_result in zip(entries, tts_results):
        entry["tts"] = tts_result if not isinstance(tts_result, Exception) else None
    
    return entries


async def run_roundtable(tts_enabled=True, topic_type="government_jobs"):
    """
    Run a roundtable discussion.
    
    Args:
        tts_enabled: Enable text-to-speech
        topic_type: "government_jobs", "travel", "tech_startup", "personal_finance", or "mental_health"
    """
    if topic_type == "travel":
        return await run_travel_roundtable(tts_enabled)
    elif topic_type == "tech_startup":
        return await run_tech_startup_roundtable(tts_enabled)
    elif topic_type == "personal_finance":
        return await run_personal_finance_roundtable(tts_enabled)
    elif topic_type == "mental_health":
        return await run_mental_health_roundtable(tts_enabled)
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

        parsed = normalize_responses(parse_responses(response), characters)
        parsed = attach_accents(parsed, characters)

        # Parallelize TTS for all speakers in this turn
        parsed = await generate_tts_batch(parsed, tts_enabled)

        for entry in parsed:
            turns.append({
                "speaker": entry["speaker"],
                "message": entry["message"],
                "tts": entry.get("tts"),
            })

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

        parsed = normalize_responses(parse_responses(response), characters)
        parsed = attach_accents(parsed, characters)

        # Parallelize TTS for all speakers in this turn
        parsed = await generate_tts_batch(parsed, tts_enabled)

        for entry in parsed:
            turns.append({
                "speaker": entry["speaker"],
                "message": entry["message"],
                "tts": entry.get("tts"),
            })

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


def normalize_responses(data, characters):
    """Ensure each entry has 'speaker' and 'message' keys and map to known characters."""
    if not isinstance(data, list):
        return []

    normalized = []
    used_speakers = set()

    for idx, entry in enumerate(data):
        if not isinstance(entry, dict):
            continue

        speaker = entry.get("speaker") or entry.get("name") or entry.get("character")
        message = entry.get("message") or entry.get("text") or entry.get("content")

        if not speaker and idx < len(characters):
            speaker = characters[idx]["name"]

        if not speaker or not message:
            continue

        normalized.append({"speaker": speaker, "message": message})
        used_speakers.add(speaker)

    # Fill missing speakers with a short placeholder to keep flow stable
    for c in characters:
        if c["name"] not in used_speakers:
            normalized.append({"speaker": c["name"], "message": "Let's continue."})

    # Keep exactly one entry per character in the same order
    final = []
    for c in characters:
        for entry in normalized:
            if entry["speaker"] == c["name"]:
                final.append(entry)
                break

    return final


def attach_accents(data, characters):
    for entry in data:
        entry.setdefault("accent", "default")
        for c in characters:
            if c["name"] == entry["speaker"]:
                entry["accent"] = c["accent"]
    return data


# ===== NEW TOPIC FUNCTIONS =====

async def run_tech_startup_roundtable(tts_enabled=True):
    topic = "Tech Startup Insights & Entrepreneurship"
    characters = TECH_STARTUP_CHARACTERS
    turns = []

    intro = (
        "Welcome to Tech Startup Roundtable! Today we're discussing key aspects of building a successful tech startup. "
        "Our panel includes Vikram (CEO), Sofia (Product Manager), Alex (CTO), and Jasmine (Growth). "
        "They'll share real-world insights on fundraising, scaling, hiring, and achieving product-market fit."
    )

    turns.append({
        "speaker": "Moderator",
        "message": intro,
        "tts": None,
    })

    for turn in range(MAX_TURNS):
        prompt = f"""
Topic: {topic}

Recent conversation:
{''.join([f"{t['speaker']}: {t['message']}\n" for t in turns[-6:]])}

Generate the NEXT TURN with natural responses from 4 startup experts.

GUIDELINES:
- Keep each response 1-3 sentences
- Share practical startup wisdom
- Mention real metrics and numbers where relevant
- React to what others said
- Ask follow-up questions when natural

Respond with JSON list of 4 objects:

[
  {{"speaker": "Vikram", "message": "Short, natural startup insight"}},
  {{"speaker": "Sofia", "message": "Short, natural startup insight"}},
  {{"speaker": "Alex", "message": "Short, natural startup insight"}},
  {{"speaker": "Jasmine", "message": "Short, natural startup insight"}}
]

NO extra text. NO markdown.
"""

        response = await call_groq([
            {"role": "system", "content": "You are 4 experienced startup founders and operators having a lively discussion about tech startups."},
            {"role": "user", "content": prompt},
        ])

        parsed = normalize_responses(parse_responses(response), characters)
        parsed = attach_accents(parsed, characters)
        parsed = await generate_tts_batch(parsed, tts_enabled)

        for entry in parsed:
            turns.append({
                "speaker": entry["speaker"],
                "message": entry["message"],
                "tts": entry.get("tts"),
            })

    return {
        "topic": topic,
        "turns": turns,
    }


async def run_personal_finance_roundtable(tts_enabled=True):
    topic = "Personal Finance & Wealth Building"
    characters = PERSONAL_FINANCE_CHARACTERS
    turns = []

    intro = (
        "Welcome to Personal Finance Roundtable! Today we're discussing money management, investing, and building wealth. "
        "Our expert panel includes Raj (Financial Advisor), Isabella (Money Coach), Marcus (Entrepreneur), and Priya (Student). "
        "They'll cover budgeting, investing, debt management, and creating financial freedom."
    )

    turns.append({
        "speaker": "Moderator",
        "message": intro,
        "tts": None,
    })

    for turn in range(MAX_TURNS):
        prompt = f"""
Topic: {topic}

Recent conversation:
{''.join([f"{t['speaker']}: {t['message']}\n" for t in turns[-6:]])}

Generate the NEXT TURN with natural responses from 4 finance experts and learners.

GUIDELINES:
- Keep each response 1-3 sentences
- Provide practical financial advice
- Mention specific numbers and strategies
- Address different perspectives (traditional vs modern approaches)
- Ask clarifying questions
- Be encouraging to those learning

Respond with JSON list of 4 objects:

[
  {{"speaker": "Raj", "message": "Short, natural finance insight"}},
  {{"speaker": "Isabella", "message": "Short, natural finance insight"}},
  {{"speaker": "Marcus", "message": "Short, natural finance insight"}},
  {{"speaker": "Priya", "message": "Short, natural finance question/response"}}
]

NO extra text. NO markdown.
"""

        response = await call_groq([
            {"role": "system", "content": "You are 4 people discussing personal finance, investing, and wealth building with different perspectives."},
            {"role": "user", "content": prompt},
        ])

        parsed = normalize_responses(parse_responses(response), characters)
        parsed = attach_accents(parsed, characters)
        parsed = await generate_tts_batch(parsed, tts_enabled)

        for entry in parsed:
            turns.append({
                "speaker": entry["speaker"],
                "message": entry["message"],
                "tts": entry.get("tts"),
            })

    return {
        "topic": topic,
        "turns": turns,
    }


async def run_mental_health_roundtable(tts_enabled=True):
    topic = "Mental Health, Wellness & Personal Growth"
    characters = MENTAL_HEALTH_CHARACTERS
    turns = []

    intro = (
        "Welcome to Mental Health & Wellness Roundtable! Today we're discussing mental well-being, stress, relationships, and personal growth. "
        "Our panel includes Dr. Arjun (Psychologist), Luna (Life Coach), James (Advocate), and Divya (Wellness Officer). "
        "They'll share practical strategies for managing anxiety, improving sleep, healthy boundaries, and building resilience."
    )

    turns.append({
        "speaker": "Moderator",
        "message": intro,
        "tts": None,
    })

    for turn in range(MAX_TURNS):
        prompt = f"""
Topic: {topic}

Recent conversation:
{''.join([f"{t['speaker']}: {t['message']}\n" for t in turns[-6:]])}

Generate the NEXT TURN with natural responses from 4 mental health and wellness experts.

GUIDELINES:
- Keep each response 1-3 sentences
- Share evidence-based mental health insights
- Be empathetic and non-judgmental
- Mention specific techniques and practices
- Address stigma around mental health openly
- Encourage seeking help when needed
- Be authentic about struggles

Respond with JSON list of 4 objects:

[
  {{"speaker": "Dr. Arjun", "message": "Short, natural mental health insight"}},
  {{"speaker": "Luna", "message": "Short, natural wellness perspective"}},
  {{"speaker": "James", "message": "Short, authentic personal experience"}},
  {{"speaker": "Divya", "message": "Short, practical organizational insight"}}
]

NO extra text. NO markdown.
"""

        response = await call_groq([
            {"role": "system", "content": "You are 4 mental health professionals and advocates having an open, empathetic discussion about mental wellness and personal growth."},
            {"role": "user", "content": prompt},
        ])

        parsed = normalize_responses(parse_responses(response), characters)
        parsed = attach_accents(parsed, characters)
        parsed = await generate_tts_batch(parsed, tts_enabled)

        for entry in parsed:
            turns.append({
                "speaker": entry["speaker"],
                "message": entry["message"],
                "tts": entry.get("tts"),
            })

    return {
        "topic": topic,
        "turns": turns,
    }