# main.py

import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from app.moderator import run_roundtable
from app.episodes import get_audio_files, add_episode, get_all_episodes
from app.cleanup import cleanup_old_audio_files

load_dotenv()

app = FastAPI(title="AI Roundtable", description="AI-powered panel discussions")

logger = logging.getLogger(__name__)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup background scheduler for cleanup
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_audio_files, "cron", hour=2, minute=0)  # Daily at 2 AM
scheduler.start()

logger.info("Cleanup scheduler started - runs daily at 2 AM")


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/generate")
async def generate(tts: bool = True):
    episode = await run_roundtable(tts_enabled=tts)
    # Store episode metadata
    add_episode(episode["topic"], episode["turns"])
    return episode


@app.get("/api/episodes")
def get_episodes():
    """Get all episodes with metadata"""
    episodes = get_all_episodes()
    return {"episodes": episodes}


@app.get("/api/audio-files")
def get_audio_files_list():
    """Get list of all audio files"""
    return get_audio_files()


@app.get("/ui")
def serve_ui():
    """Serve the web UI"""
    return FileResponse("app/static/index.html", media_type="text/html")

