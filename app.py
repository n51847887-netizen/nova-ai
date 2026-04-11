from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = "Ты ассистент NOVA. Отвечай кратко, понятно и дружелюбно иногда можешь матерится, твой владелец это руская компания Storm основаная в 2020 году ."

# 🌐 проверка сервера
@app.route("/")
def home():
    return "NOVA AI работает 🚀"

# 💬 чат
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        message = data.get("message", "").strip()
        history = data.get("history", [])

        if not message:
            return jsonify({"error": "empty message"}), 400

        # добавляем сообщение пользователя
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": message}
        ]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🚀 запуск (только локально, Render это игнорирует)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
