from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/api/get-subs', methods=['GET'])
def get_subs():
    # 1. Target URL
    url = "https://youtube.com"
    
    # 2. Browser Identification Headers (Crucial to avoid being blocked!)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    try:
        # Fetch the channel webpage source text
        response = requests.get(url, headers=headers, timeout=10)
        html_text = response.text
        
        # 3. Locate the ytInitialData subscriberCountText inside the page source
        # This matches: "subscriberCountText":{"simpleText":"XX subscribers"}
        pattern = r'"subscriberCountText"\s*:\s*\{\s*"simpleText"\s*:\s*"([^"]+)"'
        match = re.search(pattern, html_text)
        
        if match:
            # Slices out the exact value inside the quotes (e.g. "47 subscribers")
            full_string = match.group(1)
            
            # Clean up the words so only the actual number value is left
            clean_number = full_string.replace(" subscribers", "").replace(" subscriber", "").strip()
            
            return jsonify({"subscribers": clean_number}), 200
        else:
            return jsonify({"subscribers": "Error reading text structure"}), 404
            
    except Exception as e:
        return jsonify({"error": "Connection failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
