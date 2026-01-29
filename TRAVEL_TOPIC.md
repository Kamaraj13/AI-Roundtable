# Travel Destinations Podcast

## Overview
Added a new podcast topic focused on travel destinations with 4 diverse characters sharing their perspectives on 5 amazing cities around the world.

## Cities Covered
1. **Salt Lake City, USA** 🇺🇸
   - Mountain activities, skiing, Temple Square, craft breweries
   - Best season: Winter for skiing, Summer for hiking
   
2. **Abu Dhabi, UAE** 🇦🇪
   - Sheikh Zayed Grand Mosque, Louvre, desert safaris, luxury shopping
   - Best season: November to March (cooler weather)
   
3. **Chennai, India** 🇮🇳
   - Marina Beach, temples, filter coffee, seafood
   - Best season: December to February
   
4. **Bangalore, India** 🇮🇳
   - Tech hub, gardens, pub culture, pleasant weather year-round
   - Best season: October to February
   
5. **Manchester, UK** 🇬🇧
   - Football culture, music scene, industrial heritage, Northern Quarter
   - Best season: May to September

## Characters

### 1. Elena (Spanish Accent) 🇪🇸
- **Role**: Travel Blogger from Spain
- **Perspective**: Experienced traveler who has actually visited all these cities
- **Style**: Passionate, descriptive, shares vivid personal experiences
- **Voice**: Spanish accent (Monica on macOS, es on Linux)

### 2. Fatima (Arabian Accent) 🇦🇪
- **Role**: Culture Enthusiast from UAE
- **Perspective**: Extensive researcher who knows everything from books and articles
- **Style**: Knowledgeable, well-researched, shares fascinating facts
- **Voice**: Arabic accent (Majed on macOS, ar on Linux)

### 3. Priya (Indian Accent) 🇮🇳
- **Role**: Software Engineer from India
- **Perspective**: Her sister lives abroad and shares experiences
- **Style**: Friendly, relatable, shares personal stories from sister
- **Voice**: Indian English (Veena on macOS, en-in on Linux)

### 4. Carlos (Mexican Accent) 🇲🇽
- **Role**: IT Professional from Mexico
- **Perspective**: Planning to relocate, needs practical information
- **Style**: Excited, asks practical questions about living there
- **Voice**: Mexican Spanish (Juan on macOS, es-mx on Linux)

## How to Generate Travel Episodes

### Via API
```bash
# With TTS enabled (default)
curl -X POST "http://192.168.1.138:8000/generate?topic=travel"

# Without TTS (faster testing)
curl -X POST "http://192.168.1.138:8000/generate?topic=travel&tts=false"
```

### Via Web UI
1. Go to http://192.168.1.138:8000/ui (or your ngrok URL)
2. Select **"✈️ Travel Destinations"** from the dropdown
3. Click **"🎬 Generate New Episode"**
4. Wait for the episode to generate (30-60 seconds)
5. Listen to the audio players in the episode card

## Conversation Topics
The AI will discuss:
- **Places to Visit**: Must-see attractions, hidden gems, local favorites
- **Food to Try**: Local cuisine, restaurants, street food, drinks
- **Best Season**: Weather considerations, festivals, peak/off-peak times
- **Activities**: Things to do, experiences, entertainment, nightlife
- **Practical Tips**: Cost of living, transportation, safety, neighborhoods

## Conversation Style
Each character brings their unique perspective:
- **Elena**: "When I was in Abu Dhabi, the Sheikh Zayed Mosque at sunset was breathtaking!"
- **Fatima**: "According to my research, Manchester's music scene dates back to the 1960s..."
- **Priya**: "My sister in Manchester says the Northern Quarter is perfect for vintage shopping!"
- **Carlos**: "I'm curious about the cost of living in Bangalore - is it affordable for expats?"

## Update Your Server

```bash
# SSH into Ubuntu server
ssh username@192.168.1.138

# Navigate to project
cd AI-Roundtable

# Pull latest changes
git pull

# Stop current server (Ctrl+C in Terminal 1)
# Stop ngrok (Ctrl+C in Terminal 2)

# Restart both
# Terminal 1:
./start-all.sh

# Terminal 2:
./start-ngrok-tunnel.sh
```

## Testing
After restarting, test both topics:

```bash
# Test government jobs topic
curl -X POST "http://192.168.1.138:8000/generate?topic=government_jobs&tts=false"

# Test travel topic
curl -X POST "http://192.168.1.138:8000/generate?topic=travel&tts=false"
```

## Voice Quality
The same enhanced TTS settings apply to all accents:
- Speed: 140 (slower for clarity)
- Amplitude: 150 (louder, clearer)
- Word gap: 10 (100ms pauses between words)
- Pitch: 50 (natural tone)

## Tips
- Each episode has 8 turns (32 responses total)
- Each response is 1-3 sentences for natural conversation
- Characters build on each other's comments
- Mix of factual information and personal perspectives
- Discussions cover all 5 cities throughout the episode

Enjoy your global travel podcast! 🌍✈️
