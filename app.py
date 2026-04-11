from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# 🔑 ключ берётся из Render ENV
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = "Ты ассистент NOVA AI. Отвечай кратко, понятно и по делу."

# ---------------- HOME ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "NOVA AI is running 🚀"
    })

# ---------------- CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        message = data.get("message", "").strip()
        history = data.get("history", [])

        if not message:
            return jsonify({"error": "Empty message"}), 400

        history.append({"role": "user", "content": message})
        history = history[-20:]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *history
            ],
            max_tokens=1024,
            temperature=0.7,
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
