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

# If venv python is missing/broken, recreate the venv
if [ ! -x "$SCRIPT_DIR/venv/bin/python" ] || ! "$SCRIPT_DIR/venv/bin/python" -V >/dev/null 2>&1; then
    echo "⚠️  Virtual environment is broken. Recreating..."
    rm -rf venv
    python3 -m venv venv
    source venv/bin/activate
fi

# Install/upgrade dependencies
echo "📦 Checking dependencies..."
"$SCRIPT_DIR/venv/bin/pip" install -q -r app/requirements.txt

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
"$SCRIPT_DIR/venv/bin/uvicorn" app.main:app --host 0.0.0.0 --port 8000
