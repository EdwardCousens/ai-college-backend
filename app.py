from flask import Flask, request, jsonify
import openai
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
# Allow CORS for your Squarespace domain
CORS(app, origins=["https://sapphire-mandarin-p3wh.squarespace.com"])

# Set your API keys via environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
FILLOUT_API_KEY = os.getenv("FILLOUT_API_KEY")
FORM_ID = os.getenv("FILLOUT_FORM_ID", "fbeCfp8LHDus")  # Ensure this is correct

# Temporary debug: print your Fillout key (remove in production)
print("FILLOUT_API_KEY:", FILLOUT_API_KEY)

@app.route('/', methods=['GET'])
def home():
    return "🎉 Dream Ivy backend is live!"

@app.route('/process_quiz', methods=['POST'])
def process_quiz():
    data = request.get_json()
    print("📥 Received data:", data)

    submission_uuid = data.get("submissionUuid")
    if not submission_uuid:
        return jsonify({"error": "No submission UUID provided"}), 400

    # Build the Fillout API URL
    fillout_url = f"https://api.fillout.com/v1/api/forms/{FORM_ID}/submissions/{submission_uuid}"
    headers = {"Authorization": f"Bearer {FILLOUT_API_KEY}"}
    fillout_response = requests.get(fillout_url, headers=headers)
    if fillout_response.status_code != 200:
        error_msg = f"Error fetching submission from Fillout: {fillout_response.status_code} {fillout_response.text}"
        print("❌", error_msg)
        return jsonify({"error": error_msg}), fillout_response.status_code

    submission_data = fillout_response.json().get("submission", {})
    print("📤 Submission data from Fillout:", submission_data)

    processed_data = {}
    if submission_data.get("questions") and isinstance(submission_data["questions"], list):
        for question in submission_data["questions"]:
            processed_data[question["name"]] = question.get("value", "")
    else:
        print("⚠️ No questions found in submission.")

    print("📤 Processed submissionData:", processed_data)

    prompt = f"""Student Details:
School Stage: {processed_data.get('Current school stage', '')}
Strongest Subjects: {processed_data.get('Your strongest subjects, (Subject 1, Subjects 2)', '')}
School Name: {processed_data.get('School name', '')}
Intended College Degree: {processed_data.get('Intended college degree', '')}
SAT Score: {processed_data.get('SAT score', '')}
Other SAT Info: {processed_data.get('I have/will take the SAT', '')}
GPA: {processed_data.get('GPA (GPA/Maximum GPA)', '')}
Other GPA Info: {processed_data.get('I do not have a GPA', '')}
Location: {processed_data.get('Region of Studying', '')}
Co-curriculars: {processed_data.get('Co Curriculars (CC1, CC2 etc.)', '')}
Other Info: {processed_data.get('Other (Add any additional academic infomation)', '')}
Willing to Study Overseas: {processed_data.get('Are you willing to study overseas', '')}

Based on this, recommend 3-5 suitable colleges and give a brief summary of entry requirements for each.
"""

    try:
        openai_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        recommendation = openai_response.choices[0].message["content"]
        return jsonify({"recommendation": recommendation})
    except Exception as e:
        print("❌ Error from OpenAI:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()


if __name__ == '__main__':
    app.run()
