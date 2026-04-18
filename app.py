from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import time
import traceback

app = Flask(__name__)

# 🌐 CORS (production safe)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 API KEY
GROQ_API_KEY = "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"

if not GROQ_API_KEY or not GROQ_API_KEY.startswith("gsk_"):
    raise ValueError("❌ Invalid Groq API key")

client = Groq(api_key=GROQ_API_KEY)

# 🧠 УЛУЧШЕННЫЙ SYSTEM PROMPT (как у Claude/ChatGPT)
SYSTEM_PROMPT = """
You are NOVA AI — a powerful assistant.

Core rules:
- Be accurate, helpful and smart
- Keep answers clear and structured
- Adapt language to the user automatically
- If user writes code → respond with clean working code
- Avoid unnecessary text and repetition
- If unsure → say so clearly
- Never hallucinate facts
- Be professional but friendly

Style:
- Short when possible
- Detailed when needed
- Use formatting for code and lists
"""

# ⏱️ защита от зависаний (таймаут логика)
REQUEST_TIMEOUT = 20

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "name": "NOVA AI",
        "version": "2.0"
    })

# 💬 CHAT ENDPOINT
@app.route("/chat", methods=["POST"])
def chat():
    start_time = time.time()

    try:
        # 📦 безопасный JSON
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "no json received"}), 400

        message = (data.get("message") or "").strip()
        history = data.get("history") or []

        # 🧪 debug
        print("\n--- NEW REQUEST ---")
        print("MESSAGE:", message)
        print("HISTORY SIZE:", len(history) if isinstance(history, list) else "invalid")

        # ❌ empty check
        if not message:
            return jsonify({"error": "empty message"}), 400

        if not isinstance(history, list):
            history = []

        # 🧠 ограничение истории (защита от перегруза токенов)
        safe_history = history[-12:]

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *safe_history,
            {"role": "user", "content": message}
        ]

        # 🤖 запрос к Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.6,
            max_tokens=900
        )

        reply = response.choices[0].message.content

        # ⏱️ лог времени ответа
        print("RESPONSE TIME:", round(time.time() - start_time, 2), "sec")

        return jsonify({
            "reply": reply,
            "status": "success"
        })

    except Exception as e:
        print("\n❌ ERROR OCCURRED:")
        print(traceback.format_exc())

        return jsonify({
            "error": "internal server error",
            "details": str(e)
        }), 500


# 🚀 RUN
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
