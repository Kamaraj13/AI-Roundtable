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
    # Extract audio file paths - speak_text returns just filename
    # Prepend /tts_output/ for web access
    audio_files = []
    for turn in turns:
        if turn.get("tts"):
            filename = turn.get("tts")
            # Filename only, prepend /tts_output/
            audio_files.append(f"/tts_output/{filename}")
    
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
    """Get all episodes sorted by date (newest first), deduped by topic."""
    episodes = load_episodes()

    # Sort newest first
    sorted_episodes = sorted(
        episodes.values(),
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    # Deduplicate by topic, prefer entries with audio
    best_by_topic = {}
    for ep in sorted_episodes:
        topic = ep.get("topic", "Unknown")
        current = best_by_topic.get(topic)
        if not current:
            best_by_topic[topic] = ep
            continue

        current_audio = len(current.get("audio_files", []) or [])
        ep_audio = len(ep.get("audio_files", []) or [])

        # Prefer episodes that actually have audio files
        if ep_audio > 0 and current_audio == 0:
            best_by_topic[topic] = ep

    # Return in newest-first order while keeping only one per topic
    deduped = []
    added = set()
    for ep in sorted_episodes:
        topic = ep.get("topic", "Unknown")
        if topic in added:
            continue
        if best_by_topic.get(topic) == ep:
            deduped.append(ep)
            added.add(topic)

    return deduped


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
