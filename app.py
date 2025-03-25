from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
# Allow CORS for all domains (or restrict to your Squarespace domain if preferred)
CORS(app)  # To allow all origins, or use CORS(app, origins=["https://sapphire-mandarin-p3wh.squarespace.com"])

# Use your OpenAI API key from the environment variable
openai.api_key = os.getenv("sk-proj-NL-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")

@app.route('/', methods=['GET'])
def home():
    return "🎉 Dream Ivy backend is live!"

@app.route('/process_quiz', methods=['POST'])
def process_quiz():
    data = request.get_json()
    print("📥 Received data:", data)

    # Build a prompt using the data received from the frontend
    prompt = f"""Student Details:
School Stage: {data.get('school_stage', '')}
Strongest Subjects: {data.get('strongest_subjects', '')}
School Name: {data.get('school_name', '')}
Intended College Degree: {data.get('college_degree', '')}
SAT Score: {data.get('SAT_score', '')}
Other SAT Info: {data.get('other_SAT', '')}
GPA: {data.get('GPA', '')}
Other GPA Info: {data.get('other_GPA', '')}
Location: {data.get('location', '')}
Co-curriculars: {data.get('co_curriculars', '')}
Resume: {data.get('resume', '')}
Other Info: {data.get('other', '')}
Willing to Study Overseas: {data.get('overseas', '')}

Based on this, recommend 3-5 suitable colleges and give a brief summary of entry requirements for each.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        recommendation = response.choices[0].message["content"]
        return jsonify({"recommendation": recommendation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
