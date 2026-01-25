#!/bin/bash

# AI Roundtable Setup Script for Oracle VM (Ubuntu 22.04 aarch64)

set -e

echo "🚀 AI Roundtable Setup Script for Oracle VM"
echo "=========================================="

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️  This script is designed for Linux. For macOS, follow manual setup."
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python 3.11..."
sudo apt-get install -y python3.11 python3.11-venv python3-pip git

# Install TTS and audio dependencies
echo "🔊 Installing text-to-speech and audio tools..."
sudo apt-get install -y espeak-ng ffmpeg

# Install Docker (optional but recommended for aarch64)
read -p "Install Docker? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
    sudo usermod -aG docker $USER
    echo "   ℹ️  You need to logout and login for Docker group changes to take effect"
fi

# Create application directory if needed
APP_DIR="$(pwd)"
echo "📂 Working in: $APP_DIR"

# Create virtual environment
echo "🔧 Setting up Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python packages..."
pip install --upgrade pip setuptools wheel
pip install -r app/requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your GROQ_API_KEY"
    echo "   nano .env"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Create output directory
mkdir -p tts_output
chmod 755 tts_output

# Verify espeak-ng installation
echo ""
echo "🔍 Verifying espeak-ng installation..."
if command -v espeak-ng &> /dev/null; then
    echo "   ✓ espeak-ng is installed"
    espeak-ng --version | head -1
else
    echo "   ⚠️  espeak-ng not found. Try: sudo apt-get install espeak-ng"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Add your GROQ_API_KEY"
echo "3. Activate venv: source venv/bin/activate"
echo "4. Test locally: python test_local.py"
echo "5. Run server: uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo ""
echo "Or use Docker:"
echo "   docker-compose up --build"
echo ""
echo "For production with Supervisor, see DEPLOYMENT.md"
