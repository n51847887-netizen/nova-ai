from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)

# 🌐 CORS (для фронта)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 API KEY
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are NOVA AI.

Rules:
- Answer briefly and clearly
- Reply in same language as user
- Write code when needed
- No unnecessary text
"""

@app.route("/")
def home():
    return "NOVA AI работает 🚀"

# 💬 CHAT
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # 🔥 безопасное получение JSON
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "no json received"}), 400

        message = (data.get("message") or "").strip()
        history = data.get("history") or []

        print("DEBUG MESSAGE:", message)
        print("DEBUG HISTORY:", history)

        if not message:
            return jsonify({"error": "empty message"}), 400

        if not isinstance(history, list):
            history = []

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history[-10:],
            {"role": "user", "content": message}
        ]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
