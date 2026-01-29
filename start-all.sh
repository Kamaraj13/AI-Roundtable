#!/bin/bash

# start-all.sh - Fast startup script for AI Roundtable

set -e

echo "🚀 AI Roundtable - Full Startup"
echo "================================"
echo ""

# Navigate to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Quick venv check - only check if python is accessible
if ! [ -x "venv/bin/python" ]; then
    if [ ! -d "venv" ]; then
        echo "❌ Virtual environment not found. Run: python3 -m venv venv"
        exit 1
    else
        echo "⚠️  Recreating broken venv..."
        rm -rf venv
        python3 -m venv venv >/dev/null 2>&1
    fi
fi

# Activate venv
source venv/bin/activate

# Parallel: Install dependencies in background
echo "📦 Installing dependencies..."
"$SCRIPT_DIR/venv/bin/pip" install -q -r app/requirements.txt &
DEP_PID=$!

# Create directories in parallel
mkdir -p tts_output episodes_data

# Wait for pip to finish
wait $DEP_PID

echo "✅ Ready"
echo ""
echo "🎙️  Starting server on http://0.0.0.0:8000"
echo ""

# Start server with optimized settings
"$SCRIPT_DIR/venv/bin/uvicorn" app.main:app --host 0.0.0.0 --port 8000 --workers 2 --loop uvloop
