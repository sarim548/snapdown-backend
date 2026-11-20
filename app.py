"""
SnapDown - FREE backend (Flask + yt-dlp)
Only download your own videos. Respect copyright.
Platforms that block free fetching (Instagram / Facebook / X)
will return a clear error instead of a fake download.
"""
import os, re, json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def detect_platform(url):
    u = url.lower()
    if "tiktok.com" in u: return "tiktok"
    if "youtube.com" in u or "youtu.be" in u: return "youtube"
    if "instagram.com" in u: return "instagram"
    if "facebook.com" in u or "fb.watch" in u: return "facebook"
    if "x.com" in u or "twitter.com" in u: return "x"
    return "unknown"

@app.route("/")
def home():
    return jsonify({"ok": True, "service": "SnapDown free backend", "usage": "POST /api/fetch {\"url\": \"...\"}"})

@app.route("/api/fetch", methods=["POST"])
def fetch_video():
    data = request.get_json(force=True, silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url.startswith("http"):
        return jsonify({"ok": False, "error": "Paste a valid video link starting with http"}), 400

    platform = detect_platform(url)

    # Instagram / Facebook / X block free fetching - be honest about it
    if platform in ("instagram", "facebook", "x"):
        return jsonify({
            "ok": False,
            "platform": platform,
            "error": f"{platform.title()} blocks free fetching. Save your own video from the official {platform.title()} app instead.",
            "blocked": True
        })

    # Try yt-dlp first - works best for TikTok and YouTube on a server
    try:
        import yt_dlp
        ydl_opts = {"quiet": True, "noplaylist": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        formats = []
        for f in (info.get("formats") or [])[-6:]:
            if f.get("url"):
                formats.append({
                    "quality": f.get("format_note") or f.get("height") or "HD",
                    "ext": f.get("ext", "mp4"),
                    "url": f["url"]
                })
        # Best direct URL
        best_url = info.get("url") or (formats[-1]["url"] if formats else None)
        return jsonify({
            "ok": True,
            "platform": platform,
            "title": info.get("title", "Video"),
            "author": info.get("uploader", ""),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "download_url": best_url,
            "formats": formats,
            "note": "Only download your own videos."
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "platform": platform,
            "error": f"Could not fetch this video: {str(e)[:200]}. The platform may have blocked it. Try a TikTok or YouTube link.",
            "blocked": True
        }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
