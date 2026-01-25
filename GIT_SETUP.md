# AI Roundtable - Git Setup Guide

## Initialize Local Repository

```bash
cd /Users/vikki/Desktop/AI\ Roundtable/AI-Roundtable/ai-roundtable_0.02

# Initialize git
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: AI Roundtable v0.02"
```

## Connect to Remote Repository

### Option 1: GitHub

1. Create a new repository on GitHub: https://github.com/new
   - Repository name: `ai-roundtable`
   - Description: "AI-powered panel discussion simulator for government jobs in India"
   - Make it Public or Private (your choice)
   - Do NOT initialize with README (we already have one)

2. Connect local repo to GitHub:
   ```bash
   git remote add origin https://github.com/yourusername/ai-roundtable.git
   git branch -M main
   git push -u origin main
   ```

### Option 2: GitLab
Similar process, create at https://gitlab.com/projects/new

### Option 3: Gitea (Self-hosted)
If running your own Gitea instance:
```bash
git remote add origin https://your-gitea-instance.com/yourusername/ai-roundtable.git
```

## Future Commits

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

## Current Git Status
After setup, you should see:
- All app files tracked
- tts_output/ in .gitignore
- __pycache__/ in .gitignore
- .env in .gitignore (only .env.example tracked)
