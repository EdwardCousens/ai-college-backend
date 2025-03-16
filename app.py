from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Use your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "🎉 Dream Ivy backend is live!"

@app.route('/process_quiz', methods=['POST'])
def process_quiz():
    data = request.get_json()
    print("📥 Received data:", data)

    # Build a prompt that includes all the fields
    prompt = f"""Student Details:
  school_stage: submissionData["Current school stage"] || "",
          strongest_subjects: submissionData["Your strongest subjects, (Subject 1, Subjects 2)"] || "",
          school_name: submissionData["School name"] || "",
          college_degree: submissionData["Intended college degree"] || "",
          SAT_score: submissionData["SAT score"] || "",
          other_SAT: submissionData["I have/will take the SAT"] || "",
          GPA: submissionData["GPA (GPA/Maximum GPA)"] || "",
          other_GPA: submissionData["I do not have a GPA"] || "",
          location: submissionData["Region of Studying"] || "",
          co_curriculars: submissionData["Co Curriculars (CC1, CC2 etc.)"] || "",
          resume: submissionData["Upload your Resume"] || "",
          other: submissionData["Other (Add any additional academic infomation)"] || "",
          overseas: submissionData["Are you willing to study overseas"] || "",
Based on this, recommend 3-5 suitable colleges and give a brief summary of entry requirements for each.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return jsonify({"recommendation": response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
