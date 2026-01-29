#!/bin/bash

# start-ngrok-tunnel.sh - Start ngrok tunnel for global access (Quick option)

echo "🌐 Starting ngrok Tunnel..."
echo ""
echo "📝 Make sure to:"
echo "  1. Sign up at https://ngrok.com (free)"
echo "  2. Get your auth token from https://dashboard.ngrok.com/auth"
echo "  3. Run: ngrok config add-authtoken YOUR_TOKEN"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok not installed. Run: ./setup-tunneling.sh"
    exit 1
fi

# Check if authtoken is configured
if ! ngrok config check &> /dev/null; then
    echo "⚠️  ngrok not authenticated. Please run:"
    echo "   ngrok config add-authtoken YOUR_TOKEN"
    echo ""
    echo "Get your token from: https://dashboard.ngrok.com/auth"
    exit 1
fi

echo "✅ ngrok is ready. Starting tunnel to localhost:8000..."
echo ""
echo "📍 Your public URL will appear below:"
echo "================================"
ngrok http 8000
