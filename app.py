import os
import time
from collections import defaultdict, deque

from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq, APIError, APITimeoutError

app = Flask(__name__)

# =========================
# 🔒 CORS — ограничь под свой сайт в проде
# =========================
# Например: CORS(app, origins=["https://mysite.com"])
CORS(app, origins=os.environ.get("ALLOWED_ORIGIN", "*"))

# =========================
# 🔑 API KEY — только из переменных окружения!
# =========================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY не задан! На Render зайди в Settings -> Environment "
        "и добавь переменную GROQ_API_KEY со свежим ключом с console.groq.com"
    )

client = Groq(api_key=GROQ_API_KEY, timeout=15.0)  # timeout чтобы не зависало навечно

# =========================
# 🧠 SYSTEM PROMPT (короткий = быстрее и дешевле)
# =========================
# Раньше тут было 830 "фактов" (Земля вращается вокруг Солнца и т.п.) —
# это отправлялось В КАЖДЫЙ запрос и просто раздувало вход, не давая пользы.
# Модель и так это знает. Оставляем только реальные правила поведения.
SYSTEM_PROMPT = """Ты — NOVA AI, продвинутый ИИ-ассистент от Storm AI.

ПРАВИЛА:
- Отвечай на языке пользователя (русский -> русский, английский -> английский и т.д.)
- Приоритет: код и практические решения, а не теория
- Пиши чистый, современный, готовый к использованию код
- Будь точным: если чего-то не знаешь — так и скажи, не выдумывай
- Отвечай кратко и по делу, без лишней воды
- Никогда не используй грубые слова
- Текущий год: 2026"""

# =========================
# 🧠 MEMORY (in-memory, лёгкая)
# =========================
MAX_HISTORY_MESSAGES = 6  # держим последние 3 пары вопрос/ответ
memory = defaultdict(lambda: deque(maxlen=MAX_HISTORY_MESSAGES))

# =========================
# 🚀 CHAT ENGINE
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}

        message = (data.get("message") or "").strip()
        session_id = str(data.get("session_id", "default"))

        if not message:
            return jsonify({"error": "empty message"}), 400

        # Защита от слишком длинных сообщений (замедляют и повышают стоимость)
        if len(message) > 4000:
            message = message[:4000]

        history = list(memory[session_id])

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": message},
        ]

        start = time.time()

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
            max_tokens=500,
            stream=False,
        )

        elapsed = time.time() - start
        reply = response.choices[0].message.content

        memory[session_id].append({"role": "user", "content": message})
        memory[session_id].append({"role": "assistant", "content": reply})

        return jsonify({
            "reply": reply,
            "status": "success",
            "elapsed_seconds": round(elapsed, 2),
        })

    except APITimeoutError:
        return jsonify({"error": "Groq API timeout"}), 504
    except APIError as e:
        return jsonify({"error": "Groq API error", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": "server error", "details": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # Render передаёт порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
