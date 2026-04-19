from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
import time
import traceback

app = Flask(__name__, static_folder="static", template_folder="templates")

# 🌐 CORS (можно оставить, но теперь почти не нужен)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 API KEY
GROQ_API_KEY = "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"

if not GROQ_API_KEY or not GROQ_API_KEY.startswith("gsk_"):
    raise ValueError("❌ Invalid Groq API key")

client = Groq(api_key=GROQ_API_KEY)

# 🧠 SYSTEM PROMPT (оставил твой, он норм)
SYSTEM_PROMPT = """
You are NOVA AI — a next-generation intelligent assistant.

RULES:
- Reply in same language as user
- Be clear, structured, useful
- No unnecessary text
- Write code when needed
- Think step by step for complex questions
"""

# 🏠 FRONTEND (HTML САЙТ ОТДАЁТСЯ ТУТ)
@app.route("/")
def home():
    return render_template("index.html")


# 💬 CHAT API
@app.route("/chat", methods=["POST"])
def chat():
    start_time = time.time()

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "no json received"}), 400

        message = (data.get("message") or "").strip()
        history = data.get("history") or []

        # ❌ empty check
        if not message:
            return jsonify({"error": "empty message"}), 400

        if not isinstance(history, list):
            history = []

        # 🧠 ограничение памяти
        history = history[-10:]

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": message}
        ]

        # 🤖 AI REQUEST
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=900
        )

        reply = response.choices[0].message.content

        print("⏱️ RESPONSE TIME:", round(time.time() - start_time, 2), "sec")

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print("❌ ERROR:")
        print(traceback.format_exc())

        return jsonify({
            "error": "server error",
            "details": str(e)
        }), 500


# 🚀 START SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
