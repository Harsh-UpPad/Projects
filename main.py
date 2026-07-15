from flask import Flask, jsonify, render_template
import requests
import re

app = Flask(__name__)

# 1. SERVES YOUR ORIGINAL HTML PAGE (With your untouched CSS styles)
@app.route('/')
def home():
    return render_template('index.html')

# 2. FIXED SCRAPER LOGIC WITHOUT TOUCHING FRONTEND LAYOUT
@app.route('/api/get-subs', methods=['GET'])
def get_subs():
    url = "https://youtube.com"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html_text = response.text
        
        # Pattern A: Matches YouTube's newer array system -> "subscriberCountText":{"runs":[{"text":"47 subscribers"}]}
        pattern_runs = r'"subscriberCountText"\s*:\s*\{\s*"runs"\s*:\s*\[\s*\{\s*"text"\s*:\s*"([^"]+)"'
        match = re.search(pattern_runs, html_text)
        
        # Pattern B: Matches the legacy fallback -> "subscriberCountText":{"simpleText":"47 subscribers"}
        if not match:
            pattern_simple = r'"subscriberCountText"\s*:\s*\{\s*"simpleText"\s*:\s*"([^"]+)"'
            match = re.search(pattern_simple, html_text)

        if match:
            full_string = match.group(1)
            # Cleans words off the string cleanly so only the raw metric phrase displays
            clean_number = full_string.replace(" subscribers", "").replace(" subscriber", "").strip()
            return jsonify({"subscribers": clean_number}), 200
        else:
            return jsonify({"subscribers": "Format Changed"}), 404
            
    except Exception as e:
        return jsonify({"error": "Fetch failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
