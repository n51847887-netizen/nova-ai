from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# 🔑 ВСТАВЬ СВОЙ GROQ KEY СЮДА
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = "Ты ассистент NOVA AI. Отвечай кратко и понятно."

@app.route("/", methods=["GET"])
def home():
    return "NOVA AI работает 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        message = data.get("message", "")
        history = data.get("history", [])

        if not message:
            return jsonify({"error": "Empty message"}), 400

from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = "ВСТАВЬ_СЮДА_НОВЫЙ_КЛЮЧ"
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = "Ты ассистент NOVA. Отвечай кратко и понятно."

@app.route("/")
def home():
    return "NOVA AI работает 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    history = data.get("history", [])
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "empty message"}), 400

    history.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *history],
            max_tokens=1024,
            temperature=0.7,
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
