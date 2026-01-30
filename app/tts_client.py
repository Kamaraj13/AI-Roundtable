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
    "Spanish": "Monica",        # Spanish accent
    "Arabian": "Majed",         # Arabic accent (female alternative: Maged)
    "Mexican": "Juan",          # Mexican Spanish accent
    "default": "Alex",
}

VOICE_MAP_LINUX = {
    "Indian English": "en-in",  # Indian English
    "American": "en-us",         # US English
    "British": "en-gb",          # British English
    "Australian": "en-au",       # Australian English
    "Spanish": "es",             # Spanish
    "Arabian": "ar",             # Arabic
    "Mexican": "es-mx",          # Mexican Spanish
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
        # macOS: use native 'say' command with AIFF format (for local testing only)
        filename = f"{timestamp}.aiff"
        filepath = os.path.join(folder, filename)
        voice = resolve_voice(accent)
        subprocess.run(["say", "-v", voice, text, "-o", filepath], check=True)
    else:
        # Linux: use espeak-ng with improved quality settings
        filename = f"{timestamp}.wav"
        filepath = os.path.join(folder, filename)
        voice = resolve_voice(accent)
        
        # espeak-ng with quality improvements for clarity:
        # -s: speed 100 (very slow for crystal clear speech, default is 175)
        # -p: pitch 50 (natural tone)
        # -a: amplitude 200 (very loud and clear, boost from 100 default)
        # -g: word gap 15ms (increase pause between words for clarity)
        subprocess.run(
            ["espeak-ng", "-v", voice, "-s", "100", "-p", "50", "-a", "200", "-g", "15", "-w", filepath, text],
            check=True,
            capture_output=True
        )
    
    # Return just filename for storage - path construction happens at higher level
    return filename
