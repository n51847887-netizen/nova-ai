from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)

# 🔥 FIX CORS (обязательно для браузера)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 ТВОЙ КЛЮЧ (как ты просил — прямо в коде)
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You, 'nova ai', you should answer people's questions briefly without fluff, write code, and if, for example, someone writes to you in English, you respond in English politely without swearing, and if in Russian, then in Russian, and so on.

Rules:
- Answer clearly and briefly
- Be helpful
- Write code when needed
- Reply in the same language as user
- No unnecessary text
"""

@app.route("/")
def home():
    return "NOVA AI работает 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)

        message = data.get("message", "").strip()
        history = data.get("history", [])

        if not message:
            return jsonify({"error": "empty message"}), 400

        if not isinstance(history, list):
            history = []

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history[-10:],  # защита от перегруза
            {"role": "user", "content": message}
        ]

        response = client.chat.completions.create(
            model="llama-3.3-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
