from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://sapphire-mandarin-p3wh.squarespace.com"])

@app.route('/debug_submission_uuid', methods=['POST'])
def debug_submission_uuid():
    data = request.get_json()
    submission_uuid = data.get("submissionUuid")
    
    print("📥 Received submissionUuid:", submission_uuid)
    
    if not submission_uuid:
        return jsonify({"error": "No submission UUID provided"}), 400
    
    return jsonify({"message": "Submission UUID received", "submissionUuid": submission_uuid})

if __name__ == '__main__':
    app.run()


if __name__ == '__main__':
    app.run()
