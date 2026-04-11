from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = "Ты ассистент NOVA. Отвечаешь кратко и понятно."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    history = data.get("history", [])
    message = data.get("message", "").strip()

    history.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *history],
            max_tokens=1024,
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 👇 ВОТ ЭТО ДОБАВЬ
@app.route("/")
def home():
    return "NOVA AI работает 🚀"
