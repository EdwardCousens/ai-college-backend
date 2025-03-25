from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
# Allow CORS for your Squarespace domain (adjust as needed)
CORS(app, origins=["https://sapphire-mandarin-p3wh.squarespace.com"])

# Environment variables:
# OPENAI_API_KEY: your OpenAI API key (used later)
# FILLOUT_API_KEY: your Fillout API key
# FILLOUT_FORM_ID: your Fillout form id (default value provided)
FILLOUT_API_KEY = os.getenv("FILLOUT_API_KEY")
FORM_ID = os.getenv("FILLOUT_FORM_ID", "fbeCfp8LHDus")

@app.route('/debug_submission_uuid', methods=['POST'])
def debug_submission_uuid():
    data = request.get_json()
    submission_uuid = data.get("submissionUuid")
    
    print("📥 Received submissionUuid:", submission_uuid)
    
    if not submission_uuid:
        return jsonify({"error": "No submission UUID provided"}), 400
    
    # Build the Fillout API URL for the submission
    fillout_url = f"https://api.fillout.com/v1/api/forms/{FORM_ID}/submissions/{submission_uuid}"
    headers = {"Authorization": f"Bearer {FILLOUT_API_KEY}"}
    print("Requesting Fillout submission from:", fillout_url)
    
    fillout_response = requests.get(fillout_url, headers=headers)
    print("Fillout response status:", fillout_response.status_code)
    
    if fillout_response.status_code != 200:
        error_msg = f"Error fetching submission: {fillout_response.status_code} {fillout_response.text}"
        print("❌", error_msg)
        return jsonify({"error": error_msg}), fillout_response.status_code
    
    # Return the raw JSON data from Fillout
    raw_data = fillout_response.json()
    print("📤 Raw submission data:", raw_data)
    return jsonify(raw_data)

@app.route('/', methods=['GET'])
def home():
    return "🎉 Dream Ivy backend is live!"

# ... (Your existing /process_quiz endpoint remains unchanged)

if __name__ == '__main__':
    app.run()
