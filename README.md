# AI Roundtable

An AI-powered panel discussion simulator that generates dynamic conversations on government jobs and exams in India using multiple distinct personas and text-to-speech synthesis.

## Overview

AI Roundtable creates engaging multi-speaker discussions by orchestrating a panel of four AI characters with different perspectives:

- **Exam Strategist** - Strategic guidance for competitive exams
- **Serving Officer** - Real-world insights from active government officers
- **Fresh Qualifier** - Relatable perspective from recently selected candidates
- **Citizen** - Critical questioning from an informed citizen perspective

Each episode includes audio synthesis (cross-platform: macOS `say` or Linux `espeak-ng`) and JSON-formatted transcripts.

## Features

- ✅ Multi-character AI conversations using Groq API (LLaMA 3.1 8B)
- ✅ Dynamic prompt engineering with conversation history
- ✅ Cross-platform text-to-speech synthesis (macOS & Linux)
- ✅ FastAPI endpoints for easy integration
- ✅ Asynchronous request handling
- ✅ Docker support for Oracle VM deployment
- ✅ Modular, maintainable codebase

## Tech Stack

- **LLM**: Groq API (LLaMA 3.1 8B)
- **Web Framework**: FastAPI + Uvicorn
- **TTS**: macOS native `say` command (or Linux `espeak-ng`)
- **Async Runtime**: Python asyncio
- **HTTP Client**: httpx
- **Containerization**: Docker & Docker Compose

## Project Structure

```
ai-roundtable/
├── app/
│   ├── characters.py      # Character definitions and personalities
│   ├── groq_client.py     # Groq API integration
│   ├── moderator.py       # Roundtable orchestration logic
│   ├── main.py            # FastAPI application
│   ├── tts_client.py      # Cross-platform text-to-speech client
│   ├── schemas.py         # (Optional) Pydantic models
│   └── requirements.txt   # Python dependencies
├── tts_output/            # Generated audio files
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker Compose setup
├── setup-vm.sh           # Automated Oracle VM setup
├── DEPLOYMENT.md         # Oracle VM deployment guide
├── QUICKSTART.md         # Quick start guide
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.9+
- Groq API key (get from https://console.groq.com)
- For macOS: Native TTS (built-in)
- For Linux: `espeak-ng` package

### Setup Steps (Local/macOS)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kamaraj13/AI-Roundtable.git
   cd AI-Roundtable
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

### Setup Steps (Oracle VM - Ubuntu 22.04 aarch64)

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete Oracle VM setup instructions.

Quick setup:
```bash
git clone https://github.com/Kamaraj13/AI-Roundtable.git
cd AI-Roundtable
chmod +x setup-vm.sh
./setup-vm.sh
nano .env  # Add GROQ_API_KEY
```

## API Endpoints

### Health Check
```
GET /
```
Response: `{"status": "ok"}`

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

## Usage Examples

### cURL
```bash
# Health check
curl http://localhost:8000/

# Generate without TTS
curl -X POST http://localhost:8000/generate?tts=false

# Generate with TTS
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
Edit `app/characters.py` and add to the `CHARACTERS` list, then update the system prompt in `moderator.py`.

## Deployment

### Docker (Linux/Oracle VM)
```bash
docker-compose up --build
```

### Manual Setup (Ubuntu 22.04)
```bash
chmod +x setup-vm.sh
./setup-vm.sh
```

### Production with Supervisor
See [DEPLOYMENT.md](DEPLOYMENT.md) for full instructions.

## Troubleshooting

### "GROQ_API_KEY not set"
```bash
# Verify .env exists and has the key
cat .env

# Make sure python-dotenv is installed
pip install python-dotenv
```

### JSON parsing errors from Groq
- Groq occasionally returns malformed JSON
- The app has built-in retry/recovery logic
- Check `app/moderator.py:parse_responses()` for details

### TTS not generating audio files
- **macOS**: Verify `say` command works: `say "test"`
- **Linux**: Verify espeak-ng: `espeak-ng -v en-in -w test.wav "test"`
- Check file permissions in `tts_output/` directory

### Port 8000 already in use
```bash
lsof -i :8000
kill -9 <PID>
```

## Platform Compatibility

| Feature | macOS | Linux | Docker |
|---------|-------|-------|--------|
| FastAPI | ✅ | ✅ | ✅ |
| Groq API | ✅ | ✅ | ✅ |
| TTS | ✅ (say) | ✅ (espeak-ng) | ✅ (espeak-ng) |
| Docker | ✅ | ✅ | ✅ |
| aarch64 Support | ❌ | ✅ | ✅ |

## Next Steps

- [ ] Test locally
- [ ] Deploy to Oracle VM
- [ ] Add custom topics
- [ ] Create web UI
- [ ] Setup monitoring
- [ ] Add rate limiting
- [ ] Implement user authentication

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Oracle VM deployment guide
- **[GIT_SETUP.md](GIT_SETUP.md)** - Git configuration
- **[TODO.md](TODO.md)** - Setup checklist

## License

MIT

## Contact & Support

For issues or questions, check the documentation files or open an issue on GitHub.

---

**Built with ❤️ for Indian government exam aspirants**

Currently running on: Ubuntu 22.04 aarch64 (Oracle VM)
