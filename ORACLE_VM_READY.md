# Oracle VM Deployment Checklist

Your AI Roundtable application is now optimized and ready for Oracle VM deployment on Ubuntu 22.04 Minimal aarch64.

## ✅ What's Been Configured

### Code Changes
- [x] Cross-platform TTS (macOS `say` + Linux `espeak-ng`)
- [x] Version-pinned dependencies for reproducibility
- [x] Dockerfile optimized for aarch64
- [x] Setup script for automated Ubuntu 22.04 setup
- [x] Comprehensive documentation (README, DEPLOYMENT, QUICKSTART)

### GitHub Repository
- [x] Pushed to: https://github.com/Kamaraj13/AI-Roundtable
- [x] All 5 commits synced
- [x] Ready for production deployment

## 📋 Oracle VM Setup Steps

### Step 1: Create Oracle VM Instance
```
Instance Details:
- Image: Canonical Ubuntu 22.04 Minimal aarch64
- Shape: Ampere A1 Compute (ARM-based)
- Memory: 2GB minimum
- Storage: 20GB
- Networking: Open ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
```

### Step 2: SSH into VM and Clone
```bash
ssh -i your_private_key.key ubuntu@your-vm-public-ip

# Clone repository
cd ~
git clone https://github.com/Kamaraj13/AI-Roundtable.git
cd AI-Roundtable
```

### Step 3: Run Automated Setup
```bash
chmod +x setup-vm.sh
./setup-vm.sh

# When prompted, choose Y for Docker (recommended for production)
```

### Step 4: Configure Environment
```bash
# Edit .env with your GROQ_API_KEY
nano .env

# Verify it contains:
# GROQ_API_KEY=your_actual_api_key_here
```

### Step 5: Test Locally
```bash
# Activate virtual environment
source venv/bin/activate

# Test the application
python test_local.py

# Should output:
# ✅ All tests passed!
```

### Step 6: Run Application (Choose One)

#### Option A: Direct (Testing/Development)
```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Option B: Docker (Recommended for Production)
```bash
docker-compose up --build -d
```

#### Option C: Supervisor (Persistent Service)
```bash
# Follow DEPLOYMENT.md Step 4C for detailed instructions
# Sets up auto-restart and logging
```

### Step 7: Verify Deployment
```bash
# Health check
curl http://your-vm-ip:8000/

# Expected response: {"status":"ok"}
```

### Step 8: Setup Nginx Reverse Proxy (Optional but Recommended)
```bash
# Allows clean HTTP access without port number
# Follow DEPLOYMENT.md Step 5 for full setup
```

## 🔑 Key Files Reference

| File | Purpose |
|------|---------|
| `setup-vm.sh` | Automated setup for Ubuntu 22.04 |
| `Dockerfile` | Container configuration (aarch64) |
| `docker-compose.yml` | Docker orchestration |
| `DEPLOYMENT.md` | Complete deployment guide |
| `QUICKSTART.md` | Quick reference |
| `app/tts_client.py` | Cross-platform TTS (detects OS) |
| `app/requirements.txt` | Versioned dependencies |

## ⚙️ Application Architecture

```
Internet
   ↓
Nginx (Reverse Proxy) - Port 80/443
   ↓
FastAPI App - Port 8000
   ├── Groq API (LLM)
   └── espeak-ng (TTS on Linux)
   └── WAV files in tts_output/
```

## 🔍 Troubleshooting During Setup

### If setup script fails
```bash
# Run manual setup (see DEPLOYMENT.md Step 3B)
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv espeak-ng ffmpeg
python3.11 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
```

### If TTS not working
```bash
# Verify espeak-ng
which espeak-ng
espeak-ng --version

# Test it
espeak-ng -v en-in -w test.wav "Hello India"
```

### If GROQ_API_KEY not recognized
```bash
# Reload environment
source .env
echo $GROQ_API_KEY

# If empty, edit .env again
nano .env
```

### If port 8000 in use
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

## 📊 Performance Expectations

| Metric | Value |
|--------|-------|
| Episode Generation Time | 30-60 seconds |
| TTS Audio Generation | 5-10 seconds per turn |
| Total Episode Duration | ~2-3 minutes |
| Free Tier Rate Limit | ~3 requests/minute |

## 🚀 Next Steps After Successful Deployment

1. **Test the API**
   ```bash
   curl -X POST http://your-vm-ip:8000/generate?tts=false
   ```

2. **Monitor Logs**
   ```bash
   # Docker
   docker-compose logs -f
   
   # Or Supervisor
   sudo tail -f /var/log/ai-roundtable.log
   ```

3. **Setup SSL (Let's Encrypt)**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

4. **Backup Configuration**
   ```bash
   # Backup .env and tts_output
   tar -czf ai-roundtable-backup.tar.gz .env tts_output/
   ```

5. **Monitor Disk Usage**
   ```bash
   # Audio files accumulate in tts_output/
   du -sh tts_output/
   find tts_output -type f -mtime +30 -delete  # Remove files older than 30 days
   ```

## 📝 Important Notes

⚠️ **Security:**
- Never commit .env with real API keys
- Use SSH keys, not passwords for VM access
- Consider adding rate limiting before production
- Setup firewall rules appropriately

✅ **Best Practices:**
- Use Docker or Supervisor for production (not direct uvicorn)
- Monitor logs regularly
- Setup automated backups
- Keep dependencies updated
- Use Nginx as reverse proxy

💡 **Documentation:**
- DEPLOYMENT.md has detailed step-by-step instructions
- QUICKSTART.md for quick reference
- README.md for project overview
- test_local.py for testing

## 🎯 Success Indicators

You know the deployment is successful when:
1. ✅ SSH connection established to Oracle VM
2. ✅ setup-vm.sh runs without errors
3. ✅ .env configured with GROQ_API_KEY
4. ✅ test_local.py passes all tests
5. ✅ HTTP GET / returns `{"status":"ok"}`
6. ✅ Episode generation works (POST /generate)
7. ✅ TTS audio files created in tts_output/

## 📞 Support

If issues occur:
1. Check DEPLOYMENT.md troubleshooting section
2. Verify espeak-ng is installed: `which espeak-ng`
3. Check GROQ API status and rate limits
4. Review application logs
5. Test with simple curl requests first

---

**Status: Ready for Oracle VM Deployment** ✅

Repository: https://github.com/Kamaraj13/AI-Roundtable
Branch: main
Latest Commit: df268c7 (Cross-platform TTS, aarch64 optimized)

Good luck with your Oracle VM deployment! 🚀
