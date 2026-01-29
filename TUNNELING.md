# TUNNELING.md

# Making AI Roundtable Globally Accessible

This guide explains how to expose your local AI Roundtable server to the internet so people from USA, India, UAE, and everywhere can access it.

## Quick Start (Recommended: Cloudflare Tunnel)

### 1. Setup Tunneling Tools
```bash
chmod +x setup-tunneling.sh
./setup-tunneling.sh
```

### 2. Cloudflare Tunnel Setup (Stable URL)

#### First Time Only:
```bash
# Login to Cloudflare (free account)
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create ai-roundtable

# Edit config
nano ~/.cloudflared/config.yml
```

Add this to `~/.cloudflared/config.yml`:
```yaml
tunnel: ai-roundtable
ingress:
  - hostname: ai-roundtable.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
```

(Replace `yourdomain.com` with your Cloudflare domain)

#### Start Tunnel:
```bash
chmod +x start-cloudflare-tunnel.sh
./start-cloudflare-tunnel.sh
```

**Now accessible globally at:** `https://ai-roundtable.yourdomain.com/ui`

---

## Alternative: ngrok (Quick & Easy)

### 1. Setup
```bash
chmod +x setup-tunneling.sh start-ngrok-tunnel.sh
./setup-tunneling.sh
```

### 2. Get Auth Token
- Sign up: https://ngrok.com (free)
- Get token: https://dashboard.ngrok.com/auth
- Configure: `ngrok config add-authtoken YOUR_TOKEN`

### 3. Start Tunnel
```bash
./start-ngrok-tunnel.sh
```

**Your public URL appears in the terminal** (changes each restart)

---

## Full Deployment Flow

### Deploy with git pull + Tunneling Setup:
```bash
chmod +x deploy.sh
./deploy.sh
```

Then in one terminal:
```bash
./start-all.sh
```

And in another terminal:
```bash
./start-cloudflare-tunnel.sh
# or
./start-ngrok-tunnel.sh
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│         Global Users (USA, India, UAE)             │
│         Access via HTTPS tunnel                     │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │  Cloudflare/ngrok       │
        │  (Public endpoint)      │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │  Your Ubuntu Desktop    │
        │  192.168.1.138:8000     │
        │  (AI Roundtable Server) │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │  FastAPI + Groq API     │
        │  + Text-to-Speech       │
        └────────────────────────┘
```

---

## Comparison

| Feature | Cloudflare Tunnel | ngrok |
|---------|------------------|-------|
| Cost | FREE | FREE (with limits) |
| Stability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| URL Type | Static | Dynamic (changes) |
| Setup Time | 5 min | 2 min |
| Bandwidth | Unlimited | Limited (free tier) |
| Best For | Production | Testing |

---

## Troubleshooting

### Cloudflare Tunnel not working
```bash
# Check tunnel status
cloudflared tunnel list

# Check logs
cloudflared tunnel logs ai-roundtable

# Restart
./start-cloudflare-tunnel.sh
```

### ngrok not starting
```bash
# Check if authenticated
ngrok config check

# Add authtoken
ngrok config add-authtoken YOUR_TOKEN

# Restart
./start-ngrok-tunnel.sh
```

### Server not accessible
1. Ensure uvicorn is running: `./start-all.sh`
2. Check if tunnel is active (should show connection status)
3. Test locally first: `http://localhost:8000/ui`

---

## Keep Tunnel Running 24/7 (Optional)

### Using systemd service:
```bash
# Create service file
sudo nano /etc/systemd/system/ai-roundtable-tunnel.service
```

Add:
```ini
[Unit]
Description=AI Roundtable Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/AI-Roundtable
ExecStart=/usr/local/bin/cloudflared tunnel run ai-roundtable
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable ai-roundtable-tunnel.service
sudo systemctl start ai-roundtable-tunnel.service
sudo systemctl status ai-roundtable-tunnel.service
```

---

## Security Notes

⚠️ **Keep these safe:**
- `.env` file with GROQ_API_KEY
- Cloudflare tunnel credentials
- ngrok authtoken

✅ **Already protected:**
- HTTPS encryption (Cloudflare/ngrok)
- No direct IP exposure
- No port forwarding needed

---

## Next Steps

1. ✅ Run `./setup-tunneling.sh`
2. ✅ Choose Cloudflare or ngrok
3. ✅ Start tunnel: `./start-cloudflare-tunnel.sh` or `./start-ngrok-tunnel.sh`
4. ✅ Share global URL with users!

---

**Built with ❤️ for global accessibility**
