# Quick Start Guide

Get AI Roundtable running in minutes.

## Local Development (macOS)

### 1. Install Dependencies
```bash
cd ai-roundtable
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
```

### 2. Setup Environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
nano .env
```

### 3. Run Server
```bash
uvicorn app.main:app --reload
```

### 4. Test in Another Terminal
```bash
# Health check
curl http://localhost:8000

# Generate episode (without TTS)
curl -X POST http://localhost:8000/generate?tts=false

# Generate with TTS
curl -X POST http://localhost:8000/generate?tts=true
```

Or use the Python test script:
```bash
python test_local.py
```

## Oracle VM Deployment (Ubuntu)

### 1. Setup VM
```bash
# SSH into your Oracle VM
ssh -i your_key.key ubuntu@your-vm-ip

# Clone repo
git clone https://github.com/yourusername/ai-roundtable.git
cd ai-roundtable
```

### 2. Quick Setup
```bash
chmod +x setup-vm.sh
./setup-vm.sh
nano .env  # Add GROQ_API_KEY
```

### 3. Run with Supervisor (Recommended for Production)
Follow instructions in DEPLOYMENT.md (Step 4C)

### 4. Setup Nginx Reverse Proxy
Follow instructions in DEPLOYMENT.md (Step 5)

Access via: `http://your-vm-ip`

## Project Structure
```
.
├── app/
│   ├── main.py            # FastAPI app
│   ├── moderator.py       # Roundtable logic
│   ├── groq_client.py     # LLM integration
│   ├── tts_client.py      # Audio generation
│   ├── characters.py      # Character definitions
│   ├── schemas.py         # Pydantic models
│   └── requirements.txt   # Dependencies
├── README.md              # Full documentation
├── DEPLOYMENT.md          # Oracle VM setup guide
├── GIT_SETUP.md          # Git configuration
├── QUICKSTART.md         # This file
├── Dockerfile            # Docker container config
├── docker-compose.yml    # Docker Compose config
├── setup-vm.sh          # Automated VM setup
├── test_local.py        # Local testing script
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
└── tts_output/          # Generated audio files
```

## Environment Variables

Required:
- `GROQ_API_KEY` - Get from https://console.groq.com

## API Reference

### Health Check
```
GET /
Response: {"status": "ok"}
```

### Generate Roundtable
```
POST /generate?tts=true
Response:
{
  "topic": "Government Jobs and Exams in India",
  "turns": [...]
}
```

## Troubleshooting

### API Key not working
```bash
# Verify .env
cat .env

# Source .env (if running manually)
source .env
```

### Port 8000 already in use
```bash
lsof -i :8000
kill -9 <PID>
```

### Groq API rate limit
- Free tier has limited requests per minute
- Adjust MAX_TURNS in app/moderator.py
- Or upgrade your Groq plan

## Next Steps

1. ✅ Test locally
2. ✅ Set up Git repo (see GIT_SETUP.md)
3. ✅ Push to GitHub
4. ✅ Deploy to Oracle VM (see DEPLOYMENT.md)
5. Add custom topics/questions
6. Setup web UI
7. Add analytics

## Support Files

- **README.md** - Complete project documentation
- **DEPLOYMENT.md** - Full Oracle VM deployment guide
- **GIT_SETUP.md** - Git repository setup
- **test_local.py** - Testing script

---

**Ready to deploy? Follow DEPLOYMENT.md for Oracle VM setup!**
