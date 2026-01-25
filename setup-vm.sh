#!/bin/bash

# AI Roundtable Setup Script for Oracle VM (Ubuntu/Debian)

set -e

echo "🚀 AI Roundtable Setup Script"
echo "=============================="

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  This script is designed for Linux. For macOS, follow manual setup."
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python..."
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Install Docker (optional but recommended)
read -p "Install Docker? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
    sudo usermod -aG docker $USER
fi

# Install espeak for TTS (Linux alternative)
echo "🔊 Installing text-to-speech..."
sudo apt-get install -y espeak-ng ffmpeg

# Create virtual environment
echo "🔧 Setting up Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python packages..."
pip install --upgrade pip
pip install -r app/requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your GROQ_API_KEY"
    echo "   nano .env"
fi

# Create output directory
mkdir -p tts_output

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Add your GROQ_API_KEY"
echo "3. Activate venv: source venv/bin/activate"
echo "4. Run server: uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo ""
echo "Or with Docker:"
echo "1. docker-compose up --build"
