# AI Roundtable 0.03 - Asset Integration Guide

## ✅ Assets Ready

All high-quality assets are now in: `app/static/assets/`

### Background Slideshow (4 frames)
- `bg-frame-1.jpg` - 856KB
- `bg-frame-2.jpg` - 930KB  
- `bg-frame-3.jpg` - 1.0MB
- `bg-frame-4.jpg` - 775KB

### Logo
- `logo.jpg` - 1.1MB (original Adobe Express design)
- `logo.png` - 1.1MB (alternate format)

## 🎨 What's Being Built

1. **Animated Slideshow Background**
   - 4 high-quality frames cycle every 6 seconds
   - Smooth fade transitions
   - Subtle parallax/zoom effect
   - Dark overlay for text readability

2. **Theme Switcher**
   - **Bright Mode**: Light overlay, vibrant colors
   - **Dark Mode**: Dark overlay, muted elegant colors
   - Persisted in localStorage

3. **Premium UI Elements**
   - Glassmorphism cards
   - Smooth animations
   - Mac-quality buttons
   - Topic icons with gradients

## 📁 File Structure

```
app/static/
  ├── assets/
  │   ├── bg-frame-1.jpg
  │   ├── bg-frame-2.jpg
  │   ├── bg-frame-3.jpg
  │   ├── bg-frame-4.jpg
  │   ├── logo.jpg
  │   └── asset-manifest.json
  └── index.html (NEW - Production UI)
```

## 🚀 Next Steps

Once I create the new index.html, you can:
1. Start the server: `cd ai-roundtable_0.03 && ./venv/bin/uvicorn app.main:app --reload --port 8001`
2. Open: http://localhost:8001/ui
3. Test theme switching and slideshow background

## 🎯 Future Asset Needs

For complete production polish, generate these next:
- Topic cover art (1600×1600 each topic)
- Button icons (Play, Pause, Download, etc.)
- Social media preview card (1200×630)
