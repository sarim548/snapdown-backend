# SnapDown — FREE Backend

Free backend for https://snapdown-free.netlify.app
Only download your own videos. Respect copyright.

## What it does
- POST /api/fetch with {"url": "https://www.tiktok.com/..."}
- Returns title, author, duration, thumbnail, download_url and formats
- TikTok and YouTube work best
- Instagram / Facebook / X block free fetching and return a clear error

## Deploy for FREE on Render — step by step

### 1. Put these files on GitHub (free)
1. Go to github.com, sign up free, click New repository
2. Name it: snapdown-backend
3. Upload these 3 files: app.py, requirements.txt, render.yaml
   (click Add file > Upload files)

### 2. Deploy on Render (free)
1. Go to render.com, sign up free with GitHub
2. Click New + > Web Service
3. Choose your snapdown-backend repo
4. Settings:
   - Name: snapdown-backend
   - Environment: Python
   - Plan: Free
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
5. Click Create Web Service
6. Wait 3-5 minutes. Render gives you a link like:
   https://snapdown-backend-xxxx.onrender.com

Free plan note: the server sleeps after 15 minutes with no use.
The first fetch after sleeping takes 30-60 seconds to wake up. That is normal on free.

### 3. Connect it to your Netlify site
In your frontend JavaScript, set:
  const API_BASE = "https://snapdown-backend-xxxx.onrender.com";
Then call:
  fetch(API_BASE + "/api/fetch", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({url: pastedLink})
  })

### 4. Test it
Open in your browser:
  https://snapdown-backend-xxxx.onrender.com/
You should see: {"ok": true, "service": "SnapDown free backend"}

Then paste a TikTok link in your site and try download.

## Files
- app.py — Flask backend
- requirements.txt — Flask, flask-cors, yt-dlp, gunicorn
- render.yaml — Render free plan config
