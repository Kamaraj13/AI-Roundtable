#!/bin/bash

# deploy.sh - Full deployment with git pull + tunneling setup

set -e

echo "🚀 AI Roundtable - Full Deployment"
echo "===================================="
echo ""

# Navigate to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Step 1: Git pull
echo "📥 Pulling latest code from GitHub..."
git pull origin main
echo "✅ Code updated"
echo ""

# Step 2: Setup tunneling tools (only first time)
if ! command -v cloudflared &> /dev/null && ! command -v ngrok &> /dev/null; then
    echo "🌐 Setting up tunneling tools..."
    chmod +x setup-tunneling.sh
    ./setup-tunneling.sh
    echo ""
fi

# Step 3: Activate venv and install deps
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3.11 -m venv venv || python3 -m venv venv
fi

source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r app/requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 4: Setup environment
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your GROQ_API_KEY"
    echo "   nano .env"
    echo ""
fi

# Step 5: Create directories
mkdir -p tts_output
mkdir -p episodes_data

echo "✅ Setup complete!"
echo ""
echo "================================"
echo "Next: Run the server"
echo "================================"
echo ""
echo "Option 1: Start server only"
echo "   uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo ""
echo "Option 2: Start with automatic tunneling (recommended)"
echo "   chmod +x start-all.sh"
echo "   ./start-all.sh"
echo ""
echo "Then in another terminal:"
echo "   ./start-cloudflare-tunnel.sh  (or)"
echo "   ./start-ngrok-tunnel.sh"
echo ""
