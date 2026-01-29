#!/usr/bin/env python3
"""
Test audio generation and file paths locally
Run this to verify TTS and audio files are working
"""

import asyncio
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app.tts_client import speak_text
from app.episodes import add_episode
from app.characters import CHARACTERS


async def test_audio_generation():
    print("🔧 Testing Audio Generation")
    print("=" * 50)
    print()
    
    # Create tts_output if it doesn't exist
    os.makedirs("tts_output", exist_ok=True)
    
    # Test TTS with different accents
    test_cases = [
        ("Hello, this is a test of the government exam discussion system.", "American"),
        ("Hola, esto es una prueba del sistema.", "Spanish"),
        ("مرحبا، هذا اختبار للنظام", "Arabian"),
    ]
    
    filenames = []
    
    for text, accent in test_cases:
        try:
            print(f"Testing accent: {accent}")
            filename = await speak_text(text, accent)
            filepath = f"tts_output/{filename}"
            
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"  ✅ Generated: {filename} ({size} bytes)")
                filenames.append(filename)
            else:
                print(f"  ❌ File not found: {filepath}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    print()
    print(f"Generated {len(filenames)} audio files:")
    for fn in filenames:
        print(f"  - {fn}")
    
    # Test episode storage
    print()
    print("Testing Episode Storage")
    print("=" * 50)
    
    turns = [
        {"speaker": "Test Speaker 1", "message": "This is a test message", "tts": filenames[0] if filenames else None},
        {"speaker": "Test Speaker 2", "message": "This is another test", "tts": filenames[1] if len(filenames) > 1 else None},
    ]
    
    try:
        episode_id = add_episode("Test Episode", turns)
        print(f"✅ Episode created: {episode_id}")
        
        # Check if episodes.json was created
        if os.path.exists("episodes.json"):
            import json
            with open("episodes.json") as f:
                episodes = json.load(f)
            
            if episode_id in episodes:
                ep = episodes[episode_id]
                print(f"  Topic: {ep['topic']}")
                print(f"  Audio files: {ep['audio_files']}")
                print()
                print("✅ All audio paths:")
                for audio_file in ep['audio_files']:
                    print(f"  {audio_file}")
            else:
                print("❌ Episode not found in episodes.json")
        else:
            print("❌ episodes.json not found")
    except Exception as e:
        print(f"❌ Error storing episode: {str(e)}")
    
    print()
    print("=" * 50)
    print("✅ Test completed!")


if __name__ == "__main__":
    asyncio.run(test_audio_generation())
