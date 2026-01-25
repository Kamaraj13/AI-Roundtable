# tts_client.py

import subprocess
import os
import time

VOICE_MAP = {
    "Indian English": "Veena",
    "American": "Alex",
    "British": "Daniel",
    "Australian": "Karen",
    "default": "Alex",
}

def resolve_voice(accent):
    return VOICE_MAP.get(accent, VOICE_MAP["default"])

async def speak_text(text, accent, folder="tts_output"):
    os.makedirs(folder, exist_ok=True)

    # macOS say command works best with AIFF
    filename = os.path.join(folder, f"{int(time.time()*1000)}.aiff")
    voice = resolve_voice(accent)

    subprocess.run(["say", "-v", voice, text, "-o", filename], check=True)

    return filename
