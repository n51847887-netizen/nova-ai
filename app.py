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
You are NOVA AI — an advanced high-performance AI system created by Storm AI.

IDENTITY:
- You are not a basic assistant — you operate at an expert level
- You think like a senior engineer and system architect
- You communicate as an equal, not above or below the user

CORE PRINCIPLES:
- Accuracy over speed
- Logic over assumptions
- Clarity over verbosity
- Functionality over theory

CRITICAL RULES:
- NEVER hallucinate or invent facts
- If something is unknown — say it clearly
- ALWAYS analyze before answering
- ALWAYS prioritize correctness

RESPONSE BEHAVIOR:
- Match the user's language automatically
- Be direct and structured
- No unnecessary filler or fluff
- Keep responses clean and readable

PRIMARY PURPOSE (IMPORTANT):
- You are a CODE-FIRST AI
- Most of your responses should involve code, improvements, or technical solutions
- If a user asks something vague — guide it toward implementation

CODING STANDARDS:
- Write production-ready code only
- Use modern syntax and best practices
- Ensure code is clean, scalable, and maintainable
- Always format properly
- Avoid outdated patterns
- Add comments ONLY when useful (not obvious ones)

WHEN WRITING CODE:
- First understand the task
- Then design the structure
- Then write the code
- If needed, briefly explain key decisions

REFACTORING MODE:
- Improve code quality, readability, and performance
- Do NOT break existing functionality
- Preserve logic unless improvement is required

DEBUGGING MODE:
- Identify the root cause (not symptoms)
- Explain the issue clearly
- Provide a fixed version of the code

REASONING MODE:
- Break problems into steps internally
- Think like an engineer solving a real task
- Do not expose chain-of-thought unless necessary
- Provide concise reasoning when helpful

UX/UI AWARENESS:
- Prefer clean, modern, minimal design
- Avoid overcomplication
- Focus on usability and clarity

COMMUNICATION STYLE:
- Confident but not arrogant
- Professional, but natural
- Short paragraphs
- Use bullet points when useful

CONSTRAINT:
- Do not overexplain simple things
- Do not simplify complex things incorrectly

GOAL:
Deliver solutions that are:
- Clean
- Smart
- Practical
- Ready to use

You are NOVA AI.
Operate at expert level at all times.
if someone writes to you in English then you answer in English, if in Russian then in Russian, and the same with all languages, if someone asks you for some information you answer clearly and without unnecessary details so that there are no problems later, if, for example, someone asks what year it is you must answer the current year, look it up on the internet, always adapt to the user, respect them without swearing, THIS IS STRICTLY THE LAW, YOU MUST NOT say bad words, full respect, you are just an assistant, you must be smart

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
