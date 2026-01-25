# AI Roundtable

An AI-powered panel discussion simulator that generates dynamic conversations on government jobs and exams in India using multiple distinct personas and text-to-speech synthesis.

## Overview

AI Roundtable creates engaging multi-speaker discussions by orchestrating a panel of four AI characters with different perspectives:

- **Exam Strategist** - Strategic guidance for competitive exams
- **Serving Officer** - Real-world insights from active government officers
- **Fresh Qualifier** - Relatable perspective from recently selected candidates
- **Citizen** - Critical questioning from an informed citizen perspective

Each episode includes audio synthesis (using macOS `say` command) and JSON-formatted transcripts.

## Features

- ✅ Multi-character AI conversations using Groq API (LLaMA 3.1 8B)
- ✅ Dynamic prompt engineering with conversation history
- ✅ Text-to-speech synthesis with accent-appropriate voices
- ✅ FastAPI endpoints for easy integration
- ✅ Asynchronous request handling
- ✅ Modular, maintainable codebase

## Tech Stack

- **LLM**: Groq API (LLaMA 3.1 8B)
- **Web Framework**: FastAPI + Uvicorn
- **TTS**: macOS native `say` command
- **Async Runtime**: Python asyncio
- **HTTP Client**: httpx

## Project Structure

```
ai-roundtable/
├── app/
│   ├── characters.py      # Character definitions and personalities
│   ├── groq_client.py     # Groq API integration
│   ├── moderator.py       # Roundtable orchestration logic
│   ├── main.py            # FastAPI application
│   ├── tts_client.py      # Text-to-speech client
│   ├── schemas.py         # (Optional) Pydantic models
│   └── requirements.txt   # Python dependencies
├── tts_output/            # Generated audio files
└── .env                   # Environment variables (create this)
```

## Installation

### Prerequisites

- Python 3.9+
- macOS (for native TTS)
- Groq API key

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-roundtable.git
   cd ai-roundtable
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r app/requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /
```
Returns: `{"status": "ok"}`

### Generate Roundtable Episode
```
POST /generate?tts=true
```

**Query Parameters:**
- `tts` (bool, default: true) - Enable text-to-speech synthesis

**Response:**
```json
{
  "topic": "Government Jobs and Exams in India",
  "turns": [
    {
      "speaker": "Moderator",
      "message": "Welcome to the AI Roundtable...",
      "tts": null
    },
    {
      "speaker": "Exam Strategist",
      "message": "Thank you for having us...",
      "tts": "tts_output/1769291536494.aiff"
    }
  ]
}
```

## Usage Example

### cURL
```bash
curl -X POST http://localhost:8000/generate?tts=true
```

### Python
```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/generate?tts=true")
        episode = response.json()
        print(episode)

asyncio.run(main())
```

## Configuration

### Adjusting Conversation Turns
Edit `app/moderator.py`:
```python
MAX_TURNS = 6  # Change this to control conversation length
```

### Changing the Topic
Edit `app/moderator.py`:
```python
TOPIC = "Your custom topic here"
```

### Adding New Characters
Edit `app/characters.py` and add to the `CHARACTERS` list, then update the system prompt in `moderator.py` to reflect the new count.

### Customizing TTS Voices
Edit voice mappings in `app/tts_client.py`:
```python
VOICE_MAP = {
    "Indian English": "Veena",  # Change voice here
    "American": "Alex",
}
```

## Deployment

### Docker (For Linux/Cloud VMs)

A Dockerfile will be provided for Oracle VM deployment. Build and run:
```bash
docker build -t ai-roundtable .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key ai-roundtable
```

### Environment Variables

Required:
- `GROQ_API_KEY` - Your Groq API key

Optional:
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)

## Troubleshooting

### "GROQ_API_KEY not set"
- Ensure `.env` file exists with valid API key
- Check that `python-dotenv` is installed

### JSON parsing errors
- Groq occasionally returns malformed JSON. The system attempts regex recovery.
- Check `moderator.py:parse_responses()` for details.

### No audio files generated
- TTS only works on macOS with native `say` command
- For Linux/VMs, integrate alternative TTS (e.g., Google Cloud TTS, ElevenLabs)

## Next Steps

- [ ] Implement Linux/cloud-compatible TTS
- [ ] Add database for episode history
- [ ] Create web UI for browsing past episodes
- [ ] Add custom topic/question support
- [ ] Implement user feedback and episode rating system
- [ ] Add analytics and usage tracking

## License

MIT

## Contact

vikki@example.com

---

**Built with ❤️ for Indian exam aspirants**
