#!/usr/bin/env python3
"""
Local testing script for AI Roundtable
Useful for testing before deploying to Oracle VM
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"


async def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    print()


async def test_generate(tts_enabled=False):
    """Test episode generation"""
    print(f"🎬 Testing /generate endpoint (TTS: {tts_enabled})...")
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(f"{BASE_URL}/generate?tts={tts_enabled}")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Topic: {data.get('topic')}")
        print(f"   Number of turns: {len(data.get('turns', []))}")
        
        # Print first turn
        if data.get('turns'):
            first = data['turns'][0]
            print(f"\n   First turn:")
            print(f"   Speaker: {first.get('speaker')}")
            print(f"   Message: {first.get('message')[:100]}...")
            if tts_enabled and first.get('tts'):
                print(f"   TTS file: {first.get('tts')}")
    print()


async def main():
    print("=" * 60)
    print("AI Roundtable - Local Testing")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print()

    try:
        await test_health()
        await test_generate(tts_enabled=False)
        print("✅ All tests passed!")
        print()
        print("📝 Note: To test with TTS, ensure:")
        print("   - macOS native 'say' command (for macOS)")
        print("   - OR espeak-ng (for Linux)")
        print("   - Run: await test_generate(tts_enabled=True)")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Ensure server is running: uvicorn app.main:app --reload")
        print("   2. Check GROQ_API_KEY is set in .env")
        print("   3. Check internet connection to Groq API")


if __name__ == "__main__":
    asyncio.run(main())
