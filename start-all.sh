#!/bin/bash

# start-all.sh - Start AI Roundtable server + tunneling option

set -e

echo "🚀 AI Roundtable - Full Startup"
echo "================================"
echo ""

# Navigate to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run: ./setup-vm.sh"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Install/upgrade dependencies
echo "📦 Checking dependencies..."
pip install -q -r app/requirements.txt

# Create necessary directories
mkdir -p tts_output
mkdir -p episodes_data

echo "✅ Dependencies installed"
echo ""

# Start the FastAPI server
echo "🎙️  Starting AI Roundtable server..."
echo "Server running on: http://0.0.0.0:8000"
echo "Web UI: http://localhost:8000/ui"
echo ""
echo "To make it globally accessible, open another terminal and run:"
echo "  Option 1: ./start-cloudflare-tunnel.sh  (Recommended - Stable URL)"
echo "  Option 2: ./start-ngrok-tunnel.sh       (Quick & Easy)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"
echo ""

# Start uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000
