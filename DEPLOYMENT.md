# Oracle VM Deployment Guide

Complete step-by-step guide to deploy AI Roundtable on Oracle VM (Ubuntu/Debian).

## Prerequisites

1. Oracle VM Instance running Ubuntu 22.04 LTS or similar
2. SSH access to the instance
3. Groq API key (get from https://console.groq.com)

## Step 1: Connect to Your Oracle VM

```bash
ssh -i your_private_key.key ubuntu@your-vm-ip-address
```

## Step 2: Clone the Repository

```bash
cd ~
git clone https://github.com/yourusername/ai-roundtable.git
cd ai-roundtable
```

## Step 3A: Quick Setup (Automated)

```bash
chmod +x setup-vm.sh
./setup-vm.sh
```

This will:
- Update system packages
- Install Python 3.11
- Install Docker (optional)
- Install TTS dependencies (espeak-ng)
- Create virtual environment
- Install Python packages
- Create .env file

Then edit the .env file:
```bash
nano .env
# Add your GROQ_API_KEY
```

## Step 3B: Manual Setup (If Automated Script Fails)

### Install Python & Dependencies
```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3.11 python3.11-venv python3-pip
sudo apt-get install -y espeak-ng ffmpeg nginx supervisor
```

### Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r app/requirements.txt
```

### Setup Environment
```bash
cp .env.example .env
nano .env  # Add GROQ_API_KEY
mkdir -p tts_output
chmod -R 755 tts_output
```

## Step 4: Run the Application

### Option A: Direct Execution (Testing)
```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit: `http://your-vm-ip:8000`

### Option B: Docker (Production)
```bash
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
# Logout and login again
docker-compose up --build -d
```

Check logs:
```bash
docker-compose logs -f
```

### Option C: Supervisor (Persistent Service - Recommended)

Create `/etc/supervisor/conf.d/ai-roundtable.conf`:
```bash
sudo nano /etc/supervisor/conf.d/ai-roundtable.conf
```

Add:
```ini
[program:ai-roundtable]
directory=/home/ubuntu/ai-roundtable
command=/home/ubuntu/ai-roundtable/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ai-roundtable.log
environment=PATH="/home/ubuntu/ai-roundtable/venv/bin",GROQ_API_KEY="your_api_key"
```

Then:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start ai-roundtable
```

Check status:
```bash
sudo supervisorctl status ai-roundtable
sudo tail -f /var/log/ai-roundtable.log
```

## Step 5: Setup Nginx Reverse Proxy

Create `/etc/nginx/sites-available/ai-roundtable`:
```bash
sudo nano /etc/nginx/sites-available/ai-roundtable
```

Add:
```nginx
server {
    listen 80;
    server_name your-vm-ip-address;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/ai-roundtable /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Now access at: `http://your-vm-ip`

## Step 6: Setup SSL with Let's Encrypt (Optional but Recommended)

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Update nginx config to auto-redirect HTTPS:
```bash
sudo systemctl reload nginx
```

## Step 7: Configure Firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## Step 8: Monitor & Maintain

### View application logs
```bash
# If using Supervisor
sudo tail -f /var/log/ai-roundtable.log

# If using Docker
docker-compose logs -f ai-roundtable

# If direct execution
# Check terminal where uvicorn is running
```

### Update application code
```bash
cd ~/ai-roundtable
git pull origin main
source venv/bin/activate
pip install -r app/requirements.txt
sudo supervisorctl restart ai-roundtable  # or docker-compose restart
```

### Monitor disk usage (TTS output files)
```bash
du -sh tts_output/
# Clean old files older than 30 days:
find tts_output -type f -mtime +30 -delete
```

## Testing the Deployment

### Health check
```bash
curl http://your-vm-ip/
# Expected: {"status":"ok"}
```

### Generate episode
```bash
curl -X POST http://your-vm-ip/generate?tts=true
# Expected: JSON with episode data
```

### Test with Python
```python
import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://your-vm-ip/generate?tts=true")
        print(response.json())

asyncio.run(test())
```

## Troubleshooting

### Port 8000 already in use
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

### GROQ_API_KEY not set
```bash
# Check .env file
cat .env

# Verify environment variable
echo $GROQ_API_KEY

# If using Supervisor, update the conf file and restart
sudo supervisorctl restart ai-roundtable
```

### TTS not working
- On Linux, TTS uses espeak-ng instead of macOS `say`
- If audio files not generating, check espeak-ng installation:
  ```bash
  which espeak-ng
  espeak-ng "Test message" -w test.wav
  ```

### High CPU usage
- Check if API calls are stuck
- Review Groq API status
- Monitor with: `top` or `htop`

## Next Steps

1. Setup automatic backups of `tts_output/`
2. Configure monitoring/alerting (e.g., Datadog, New Relic)
3. Setup CI/CD pipeline (GitHub Actions) for auto-deployment
4. Add rate limiting and authentication
5. Scale with load balancer if needed

## Support

For issues, check logs and reference the main README.md
