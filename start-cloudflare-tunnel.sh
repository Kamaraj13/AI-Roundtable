#!/bin/bash

# start-cloudflare-tunnel.sh - Start Cloudflare Tunnel for global access

echo "🌐 Starting Cloudflare Tunnel..."
echo ""
echo "Make sure you have:"
echo "  1. Run: cloudflared tunnel login"
echo "  2. Run: cloudflared tunnel create ai-roundtable"
echo "  3. Edited ~/.cloudflared/config.yml"
echo ""

# Check if tunnel exists
if cloudflared tunnel list | grep -q "ai-roundtable"; then
    echo "✅ Tunnel exists. Starting..."
    cloudflared tunnel run ai-roundtable
else
    echo "❌ Tunnel 'ai-roundtable' not found."
    echo "Run these commands first:"
    echo "  cloudflared tunnel login"
    echo "  cloudflared tunnel create ai-roundtable"
    exit 1
fi
