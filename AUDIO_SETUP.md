# Audio Files Setup & Troubleshooting Guide

## Quick Fix Steps (Do This First!)

### On Your Ubuntu Server (192.168.1.138)

**Terminal 1:**
```bash
# SSH into the server
ssh username@192.168.1.138

# Navigate to project
cd AI-Roundtable

# Pull latest fixes
git pull

# Stop any existing server (Ctrl+C)

# Activate virtual environment
source venv/bin/activate

# Clear old data
rm -f episodes.json  # This removes old episode metadata
# Keep tts_output directory - don't delete those audio files

# Start fresh
./start-all.sh
```

**Terminal 2:**
```bash
# In another terminal, restart ngrok
ssh username@192.168.1.138
cd AI-Roundtable
source venv/bin/activate

# Stop old tunnel (Ctrl+C)
./start-ngrok-tunnel.sh
```

## What Was Fixed

### 1. Audio Path Handling ✅
**Before:** Complex path logic with multiple edge cases  
**After:** Simple `filename → /tts_output/filename`

### 2. TTS Client ✅
- Returns just the filename (e.g., `1234567890.wav`)
- Actual file saved with full path internally

### 3. Episodes Storage ✅
- Takes filename from TTS
- Automatically prepends `/tts_output/` for web access
- Stores in episodes.json with correct URLs

## Testing Locally (macOS)

Test the audio generation locally before deploying:

```bash
cd "/Users/vikki/Desktop/AI Roundtable/AI-Roundtable/ai-roundtable_0.02"
python3 test_audio.py
```

This will:
- ✅ Generate test audio files
- ✅ Create episode metadata
- ✅ Show correct audio paths
- ✅ Verify everything works

**Expected Output:**
```
🔧 Testing Audio Generation
==================================================

Testing accent: American
  ✅ Generated: 1234567890.aiff (123456 bytes)
...
✅ Episode created: 1234567890123
  Topic: Test Episode
  Audio files: ['/tts_output/1234567890.aiff', ...]

✅ All audio paths:
  /tts_output/1234567890.aiff
  /tts_output/1234567891.aiff
```

## Verification on Ubuntu Server

After restarting the server, test:

```bash
# Test without TTS (faster)
curl -X POST "http://192.168.1.138:8000/generate?topic=government_jobs&tts=false"

# Check if episodes.json was created
cat episodes.json | python3 -m json.tool | head -30

# Check audio files directory
ls -lh tts_output/ | head -20

# Check file sizes
du -sh tts_output/
```

## What to Expect

### Government Jobs Episode
- Topic: **"Government Jobs and Exams in India"**
- Characters: Exam Strategist, Serving Officer, Fresh Qualifier, Citizen
- Audio files: One per speaker response (~32 total)

### Travel Episode
- Topic: **"Our Favorite Travel Destinations"**
- Characters: Elena (Spanish), Fatima (Arabian), Priya (Indian), Carlos (Mexican)
- Audio files: One per speaker response (~32 total)
- Cities: Salt Lake City, Abu Dhabi, Chennai, Bangalore, Manchester

## Audio File Location

Files are saved in:
```
/path/to/project/tts_output/
```

Web accessible at:
```
http://192.168.1.138:8000/tts_output/FILENAME
http://your-ngrok-url.ngrok-free.dev/tts_output/FILENAME
```

## Debugging

If audio files still don't appear:

### 1. Check Server Logs
```bash
# In Terminal 1 where server is running
# Look for these messages:
# - "Generating episode: topic=..."
# - "Episode created: ..."
# - Any error messages
```

### 2. Verify TTS Installation (Ubuntu)
```bash
# Check if espeak-ng is installed
espeak-ng --version

# If not installed:
sudo apt-get update
sudo apt-get install espeak-ng ffmpeg
```

### 3. Check Permissions
```bash
# Ensure tts_output directory is writable
chmod 755 tts_output/
```

### 4. Check GROQ_API_KEY
```bash
# Make sure your .env file has this
cat .env | grep GROQ_API_KEY
```

## File Naming

- **macOS**: `1234567890.aiff`
- **Linux**: `1234567890.wav`

Both are valid and will play in modern browsers.

## Browser Compatibility

All modern browsers support:
- ✅ AIFF (Safari, Chrome)
- ✅ WAV (Firefox, Chrome, Safari)
- ✅ MP3 (All browsers)

The HTML player tries all three formats for maximum compatibility.

## Clean Slate

If you want to completely reset:

```bash
# Stop the server
# Then:

# Remove old data
rm -f episodes.json
rm -f episodes.json.bak

# Keep tts_output directory
# But you can clear old audio files if disk space is an issue:
rm -f tts_output/*.wav tts_output/*.aiff

# Restart
./start-all.sh
```

## Success Indicators

✅ Episode generates without errors  
✅ episodes.json file created with episode data  
✅ Audio files appear in tts_output/ directory  
✅ Web UI shows episode with audio players  
✅ Audio players have "Turn 1", "Turn 2", etc. labels  
✅ Clicking play button works  

If all these are ✅, then audio is working correctly!

---

Need more help? Check the server logs in Terminal 1 - errors will show there.
