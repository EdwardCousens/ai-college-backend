from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "🎉 Dream Ivy backend is live!"

@app.route('/process_quiz', methods=['POST'])
def process_quiz():
    data = request.get_json()

    print("📥 Received data:", data)


    prompt = f"""Student Details:
    Marks: {data.get('marks')}
    Location: {data.get('location')}
    Year Level: {data.get('year_level')}
    Considering studying overseas: {data.get('overseas')}
    Ideal Courses: {data.get('courses')}
    Ideal Universities: {data.get('universities')}

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

