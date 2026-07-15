from flask import Flask, jsonify, render_template
import requests
import re

# Standard instantiation looks directly for the root 'templates' folder
app = Flask(__name__)

# 1. SERVE THE HTML HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# 2. THE WEB SCRAPER API ENDPOINT
@app.route('/api/get-subs', methods=['GET'])
def get_subs():
    url = "https://youtube.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html_text = response.text
        
        # Regex search targeting YouTube's public variable
        pattern = r'"subscriberCountText"\s*:\s*\{\s*"simpleText"\s*:\s*"([^"]+)"'
        match = re.search(pattern, html_text)
        
        if match:
            full_string = match.group(1)
            # Remove trailing phrase characters
            clean_number = full_string.replace(" subscribers", "").replace(" subscriber", "").strip()
            return jsonify({"subscribers": clean_number}), 200
        else:
            return jsonify({"subscribers": "Unavailable"}), 404
            
    except Exception as e:
        return jsonify({"error": "Failed scraping", "details": str(e)}), 500

# For running on your local machine
if __name__ == '__main__':
    app.run(port=5000)
