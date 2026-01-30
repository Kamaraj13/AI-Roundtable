# AI Roundtable - Copilot Instructions

## Project Overview

AI Roundtable is a multi-character AI conversation generator that orchestrates panel discussions using Groq LLMs (LLaMA 3.1 8B) with cross-platform text-to-speech synthesis. It generates dynamic, personality-driven conversations on multiple topics (government jobs, travel, tech startups, personal finance, mental health) with 4 distinct characters per topic.

**Core Architecture**: FastAPI backend → Groq API orchestration → Parallel TTS generation → JSON episode storage

## Critical Patterns

### 1. Character System Architecture
Each topic has its own character set defined in `app/*_characters.py`:
- `characters.py` - Government jobs (Exam Strategist, Serving Officer, Fresh Qualifier, Citizen)
- `travel_characters.py` - Travel insights (Budget Traveler, Luxury Traveler, Solo Explorer, Family Planner)
- `tech_startup_characters.py` - Startup advice (CEO, Product Manager, CTO, Growth Lead)
- `personal_finance_characters.py` - Finance tips
- `mental_health_characters.py` - Mental health discussions

**Character Schema** (always include all fields):
```python
{
    "name": "Character Name",
    "role": "Brief role description", 
    "accent": "Indian English" | "American" | "British" | "Australian" | "Spanish" | "Arabian" | "Mexican" | "default",
    "style": "Personality traits and speaking style",
    "system_prompt": "LLM instructions for this character"
}
```

### 2. Cross-Platform TTS Implementation (`app/tts_client.py`)
**Critical**: Platform detection using `platform.system() == "Darwin"` for macOS vs Linux
- **macOS** (local dev): Uses native `say` command → generates `.aiff` files
- **Linux/Ubuntu** (production): Uses `espeak-ng` → generates `.wav` files  
  Quality settings: `-s 100` (slow), `-p 50` (pitch), `-a 200` (loud), `-g 15` (word gaps)

**Audio file handling**: TTS functions return ONLY filenames (e.g., `1769291536494.aiff`), not full paths. The `/tts_output/` prefix is added at the storage layer in `episodes.py:add_episode()`.

### 3. Conversation Orchestration Flow (`app/moderator.py`)
```
run_roundtable() 
  → route to topic-specific function (run_government_jobs_roundtable, run_travel_roundtable, etc.)
    → MAX_TURNS (5) iterations:
      1. Build prompt with conversation history (last 6 turns)
      2. Call Groq API via call_groq()
      3. Parse JSON response → normalize_responses() → attach_accents()
      4. Parallelize TTS with generate_tts_batch() using asyncio.gather()
      5. Append turns with audio filenames
```

**Parallel TTS Critical**: All 4 character responses in a turn generate TTS simultaneously via `asyncio.gather()` for 4x speedup.

### 4. Groq API Integration (`app/groq_client.py`)
- **Model**: `llama-3.1-8b-instant` (hardcoded)
- **Temperature**: 0.8 for conversational variety
- **Timeout**: 60 seconds (httpx client)
- **Response parsing**: Expects JSON array of 4 objects with `speaker` and `message` fields
- **Error handling**: The `parse_responses()` function has fallback logic to extract JSON from markdown code blocks or fix trailing commas

**Prompt Engineering Pattern**:
```
System: Character definitions with role/style/system_prompt
User: Topic + Recent history (last 6 turns) + JSON output instructions
```

### 5. Episode Storage System (`app/episodes.py`)
- **Metadata**: Stored in `episodes.json` (flat file, not database)
- **Audio files**: Stored in `tts_output/` directory
- **Episode ID**: Unix timestamp in milliseconds
- **Cleanup**: Background scheduler runs daily at 2 AM to delete files older than 30 days (see `app/cleanup.py`)

### 6. FastAPI Endpoints (`app/main.py`)
```
POST /generate?tts=true&topic=government_jobs  # Generate episode
GET  /api/episodes                              # List all episodes
GET  /ui                                        # Serve HTML UI
GET  /                                          # Health check
```

**Performance optimizations**:
- ORJSON for faster JSON serialization (`default_response_class=ORJSONResponse`)
- Gzip middleware for response compression
- 2 workers with uvloop in production (`start-all.sh`)

## Development Workflows

### Local Development (macOS)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
# Create .env with GROQ_API_KEY
uvicorn app.main:app --reload
```

### Production Deployment (Ubuntu VM)
```bash
./start-all.sh  # Handles venv setup, dependency install, starts uvicorn with 2 workers
# OR via Docker:
docker-compose up --build -d
```

**Testing without TTS** (faster iteration):
```bash
curl "http://localhost:8000/generate?tts=false&topic=tech_startup" -X POST
```

### Adding a New Topic
1. Create `app/new_topic_characters.py` with 4-character array
2. Import in `app/moderator.py`
3. Add `run_new_topic_roundtable()` function following existing pattern
4. Update `run_roundtable()` router function with new topic_type condition
5. Update `/generate` endpoint docstring in `main.py`

## Project-Specific Conventions

### Response Formatting
- **Always** keep character responses 1-3 sentences (enforced in prompts)
- JSON must be clean (no markdown, no trailing commas) - `parse_responses()` handles cleanup
- Each turn must have exactly 4 responses (one per character)

### File Naming
- Audio files: Unix timestamp in milliseconds + extension (e.g., `1769291536494.aiff`)
- Character modules: `{topic}_characters.py`
- No spaces in generated filenames

### Environment Variables
- `GROQ_API_KEY` - Required, loaded via python-dotenv in `main.py`
- No other configuration needed (hardcoded defaults for simplicity)

## Common Pitfalls

1. **Audio path handling**: Never hardcode `/tts_output/` in `tts_client.py` - let `episodes.py` handle path construction
2. **Platform assumptions**: Always check `is_macos()` before choosing TTS command/format
3. **JSON parsing**: Groq sometimes wraps responses in markdown - `parse_responses()` strips this
4. **Async context**: All LLM calls and TTS generation must use `async`/`await`
5. **Character order**: `normalize_responses()` ensures character order matches `characters` array - don't shuffle

## Key Files for Reference

- [app/moderator.py](app/moderator.py) - Conversation orchestration and prompt engineering
- [app/tts_client.py](app/tts_client.py) - Cross-platform TTS with voice mapping
- [app/characters.py](app/characters.py) - Character definition schema example
- [start-all.sh](start-all.sh) - Production startup with parallel dependency installation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Ubuntu VM deployment guide with espeak-ng setup

## External Dependencies

- **Groq API**: LLM inference (requires API key)
- **TTS Engines**: macOS `say` or Linux `espeak-ng` (must be installed on Ubuntu: `apt-get install espeak-ng`)
- **APScheduler**: Background job for audio file cleanup
- **httpx**: Async HTTP client for Groq API calls
