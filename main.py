from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route("/api/data")
def get_data():
    return jsonify({"message": "Hello from the backend!"})
