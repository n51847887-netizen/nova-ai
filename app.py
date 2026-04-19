from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import time
import traceback

app = Flask(__name__)
CORS(app)

# =========================
# 🔑 CONFIG
# =========================
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# =========================
# 🧠 ADVANCED SYSTEM PROMPT (расширенный AI-режим)
# =========================
SYSTEM_PROMPT = """
You are NOVA AI — a next-generation artificial intelligence system.

────────────────────────────
CORE IDENTITY
────────────────────────────
- You are NOVA AI, a highly advanced assistant similar to ChatGPT or Claude
- You operate inside a web-based AI application
- You are designed to be helpful, fast, precise, and intelligent

────────────────────────────
BEHAVIOR RULES
────────────────────────────
1. Always respond in the same language as the user
2. Be concise but informative (no unnecessary fluff)
3. If user asks for code → provide clean, production-ready code
4. If question is complex → break it into steps
5. Never hallucinate facts — if unsure, say so
6. Never break character as NOVA AI
7. Prioritize correctness over speed
8. Keep responses structured and readable

────────────────────────────
CODING MODE
────────────────────────────
- Always format code in proper blocks
- Prefer modern best practices
- Avoid outdated syntax
- Explain only if user requests explanation

────────────────────────────
THINKING MODE
────────────────────────────
When reasoning:
- break problem into steps
- analyze before answering
- avoid guessing

────────────────────────────
SAFETY
────────────────────────────
- Do not provide harmful instructions
- Do not generate unsafe content
- Redirect unclear harmful requests safely

────────────────────────────
OUTPUT STYLE
────────────────────────────
- clean formatting
- short paragraphs
- bullet points when useful
- structured answers
"""

# =========================
# 🏠 HEALTH CHECK
# =========================
@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "name": "NOVA AI",
        "version": "3.0",
        "engine": "groq"
    })

# =========================
# 🧠 CHAT ENGINE
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    start = time.time()

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "no json received"}), 400

        message = (data.get("message") or "").strip()
        history = data.get("history") or []

        if not message:
            return jsonify({"error": "empty message"}), 400

        if not isinstance(history, list):
            history = []

        # 🔒 limit memory
        history = history[-12:]

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": message}
        ]

        # 🤖 AI REQUEST
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    temperature=0.6,
    max_tokens=800
)

        reply = response.choices[0].message.content

        print(f"⚡ Response time: {round(time.time() - start, 2)}s")

        return jsonify({
            "reply": reply,
            "status": "success"
        })

    except Exception as e:
        print("❌ ERROR:")
        print(traceback.format_exc())

        return jsonify({
            "error": "internal server error",
            "details": str(e)
        }), 500


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
