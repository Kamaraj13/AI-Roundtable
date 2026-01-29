# episodes.py

import os
import json
from datetime import datetime
from typing import List
from pathlib import Path

EPISODES_FILE = "episodes.json"
TTS_OUTPUT_DIR = "tts_output"


def load_episodes() -> dict:
    """Load episodes metadata"""
    if os.path.exists(EPISODES_FILE):
        try:
            with open(EPISODES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_episodes(episodes: dict):
    """Save episodes metadata"""
    with open(EPISODES_FILE, 'w') as f:
        json.dump(episodes, f, indent=2)


def add_episode(topic: str, turns: list) -> str:
    """Add a new episode and return episode ID"""
    episode_id = str(int(datetime.now().timestamp() * 1000))
    
    episodes = load_episodes()
    # Extract audio file paths and prepend /tts_output/ for web access
    audio_files = []
    for turn in turns:
        if turn.get("tts"):
            # If path starts with tts_output/, prepend /
            # Otherwise if it's just a filename, prepend /tts_output/
            path = turn.get("tts")
            if path.startswith("tts_output/"):
                audio_files.append("/" + path)
            elif not path.startswith("/"):
                audio_files.append("/tts_output/" + os.path.basename(path))
            else:
                audio_files.append(path)
    
    episodes[episode_id] = {
        "id": episode_id,
        "topic": topic,
        "created_at": datetime.now().isoformat(),
        "turns_count": len(turns),
        "audio_files": audio_files
    }
    
    save_episodes(episodes)
    return episode_id


def get_all_episodes() -> List[dict]:
    """Get all episodes sorted by date (newest first)"""
    episodes = load_episodes()
    return sorted(
        episodes.values(),
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )


def get_episode(episode_id: str) -> dict:
    """Get a specific episode"""
    episodes = load_episodes()
    return episodes.get(episode_id)


def get_audio_files():
    """List all audio files in tts_output/"""
    files = []
    if os.path.exists(TTS_OUTPUT_DIR):
        for f in os.listdir(TTS_OUTPUT_DIR):
            filepath = os.path.join(TTS_OUTPUT_DIR, f)
            if os.path.isfile(filepath):
                files.append({
                    "name": f,
                    "path": filepath,
                    "size": os.path.getsize(filepath),
                    "created": datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
                })
    return sorted(files, key=lambda x: x["created"], reverse=True)
