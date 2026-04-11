from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = "Ты ассистент NOVA. Отвечай кратко."

@app.route("/")
def home():
    return "NOVA AI работает 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        max_tokens=1024,
        temperature=0.7,
    )

    return jsonify({
        "reply": response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
