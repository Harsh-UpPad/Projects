from flask import Flask, render_template, jsonify

app = Flask(__name__)

# This route serves your HTML page when you visit the main URL
@app.route("/")
def home():
    return render_template("index.html")

# This is an optional backend API route for your data
@app.route("/api/data")
def get_data():
    return jsonify({"status": "success", "message": "Connected to backend!"})
