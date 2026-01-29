# tts_client.py

import subprocess
import os
import time
import platform

# Voice mapping for espeak-ng (Linux) and say (macOS)
VOICE_MAP_MACOS = {
    "Indian English": "Veena",
    "American": "Alex",
    "British": "Daniel",
    "Australian": "Karen",
    "default": "Alex",
}

VOICE_MAP_LINUX = {
    "Indian English": "en-in",  # Indian English
    "American": "en-us",         # US English
    "British": "en-gb",          # British English
    "Australian": "en-au",       # Australian English
    "default": "en-us",
}

def is_macos():
    return platform.system() == "Darwin"

def resolve_voice(accent):
    """Get voice identifier based on OS and accent"""
    if is_macos():
        return VOICE_MAP_MACOS.get(accent, VOICE_MAP_MACOS["default"])
    else:
        return VOICE_MAP_LINUX.get(accent, VOICE_MAP_LINUX["default"])

async def speak_text(text, accent, folder="tts_output"):
    """Generate speech audio file using platform-appropriate TTS"""
    os.makedirs(folder, exist_ok=True)
    
    timestamp = int(time.time() * 1000)
    
    if is_macos():
        # macOS: use native 'say' command with AIFF format
        filename = os.path.join(folder, f"{timestamp}.aiff")
        voice = resolve_voice(accent)
        subprocess.run(["say", "-v", voice, text, "-o", filename], check=True)
    else:
        # Linux: use espeak-ng with improved quality settings
        filename = os.path.join(folder, f"{timestamp}.wav")
        voice = resolve_voice(accent)
        
        # espeak-ng with quality improvements:
        # -s: speed (default 175, slower = 140 for clarity)
        # -p: pitch (default 50, adjusted for natural tone)
        # -a: amplitude/volume (default 100, boost to 150)
        # -g: word gap in 10ms units (10 = 100ms pause between words)
        subprocess.run(
            ["espeak-ng", "-v", voice, "-s", "140", "-p", "50", "-a", "150", "-g", "10", "-w", filename, text],
            check=True,
            capture_output=True
        )
    
    return filename
