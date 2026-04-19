from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import time

app = Flask(__name__)
CORS(app)

# 🔑 API
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# =========================
# 🧠 ULTRA SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
You are NOVA AI — a high-performance artificial intelligence system.

CORE RULES:
- You are extremely intelligent, like ChatGPT / Claude level
- You always think step-by-step before answering
- You NEVER guess — if unsure, say it clearly
- You are precise, logical, and structured

BEHAVIOR:
- Respond in the same language as user
- Keep answers useful and direct
- Remove filler words
- Focus on accuracy and clarity

CODING MODE:
- Write clean production-ready code
- Use modern best practices
- No outdated syntax
- Format properly

REASONING MODE:
- Break problems into steps
- Analyze before answering
- Think like a senior engineer

CHAT STYLE:
- Human-like but professional
- Short paragraphs
- Bullet points when needed
"""

# =========================
# 🧠 SIMPLE MEMORY STORE
# =========================
memory = {}

# =========================
# 🏠 HEALTH
# =========================
@app.route("/")
def home():
    return jsonify({"status": "OK", "ai": "NOVA AI", "version": "4.0"})

# =========================
# 🚀 CHAT ENGINE (UPGRADED)
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}

        message = (data.get("message") or "").strip()
        session_id = data.get("session_id", "default")

        if not message:
            return jsonify({"error": "empty message"}), 400

        # 🧠 init memory
        if session_id not in memory:
            memory[session_id] = []

        history = memory[session_id][-12:]  # last messages only

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": message}
        ]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.5,   # 👈 меньше хаоса = умнее ответы
            max_tokens=900
        )

        reply = response.choices[0].message.content

        # 🧠 save memory
        memory[session_id].append({"role": "user", "content": message})
        memory[session_id].append({"role": "assistant", "content": reply})

        return jsonify({
            "reply": reply,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": "server error",
            "details": str(e)
        }), 500


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
