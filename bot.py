from flask import Flask, request
import requests
import random

app = Flask(__name__)

# Token de Telegram
TELEGRAM_TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Lista de preguntas y respuestas
questions = [
    {
        "question": "¿Cuál es la capital de Francia?",
        "answers": ["Madrid", "París", "Roma"],
        "correct": "París"
    },
    {
        "question": "¿En qué año llegó el hombre a la luna?",
        "answers": ["1965", "1969", "1972"],
        "correct": "1969"
    },
    {
        "question": "¿Cuál es el planeta más cercano al sol?",
        "answers": ["Mercurio", "Venus", "Tierra"],
        "correct": "Mercurio"
    }
]

# Función para generar botones de respuesta
def create_buttons(answers):
    return [{"text": answer, "callback_data": answer} for answer in answers]

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    print(update)  # Para depuración

    # Si es un mensaje normal
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            question = random.choice(questions)
            question_text = question["question"]
            answers = question["answers"]

            keyboard = {
                "inline_keyboard": [create_buttons(answers)]
            }

            requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": question_text,
                "reply_markup": keyboard
            })

    # Si es una respuesta (callback query)
    elif "callback_query" in update:
        callback = update["callback_query"]
        callback_data = callback["data"]
        chat_id = callback["message"]["chat"]["id"]
        question_text = callback["message"]["text"]

        # Responder al callback (obligatorio)
        requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={
            "callback_query_id": callback["id"]
        })

        # Buscar la pregunta y la respuesta correcta
        correct_answer = next((q["correct"] for q in questions if q["question"] == question_text), None)

        if correct_answer:
            if callback_data == correct_answer:
                response_text = "✅ ¡Correcto!"
            else:
                response_text = "❌ ¡Incorrecto!"

            requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": response_text
            })

    return "OK", 200

@app.route('/')
def index():
    return "🤖 ¡El bot de preguntas está funcionando!"

if __name__ == "__main__":
    app.run(debug=True)





