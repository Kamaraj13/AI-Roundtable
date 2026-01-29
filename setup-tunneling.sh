#!/bin/bash

# setup-tunneling.sh - Setup Cloudflare Tunnel and ngrok for global access

set -e

echo "================================"
echo "AI Roundtable - Tunneling Setup"
echo "================================"
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "📦 Installing Cloudflare Tunnel..."
    curl -L --output /tmp/cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i /tmp/cloudflared.deb
    rm /tmp/cloudflared.deb
    echo "✅ Cloudflare Tunnel installed"
else
    echo "✅ Cloudflare Tunnel already installed"
fi

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "📦 Installing ngrok..."
    curl -L https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz | tar xz
    sudo mv ngrok /usr/local/bin/ 2>/dev/null || mv ngrok ~/ngrok
    echo "✅ ngrok installed"
else
    echo "✅ ngrok already installed"
fi

echo ""
echo "================================"
echo "Tunneling Tools Setup Complete!"
echo "================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "Option 1: Cloudflare Tunnel (Recommended - Stable URL)"
echo "   cloudflared tunnel login"
echo "   cloudflared tunnel create ai-roundtable"
echo "   # Edit ~/.cloudflared/config.yml with your domain"
echo "   ./start-cloudflare-tunnel.sh"
echo ""
echo "Option 2: ngrok (Quick & Easy - Free tier)"
echo "   ./start-ngrok-tunnel.sh"
echo ""
