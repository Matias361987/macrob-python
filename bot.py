from flask import Flask, request
import requests
import random

app = Flask(__name__)

# Token de Telegram
TELEGRAM_TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

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
    buttons = []
    for answer in answers:
        buttons.append({
            "text": answer,
            "callback_data": answer
        })
    return buttons

# Función para manejar el webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()

    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Si el mensaje es "/start", inicia el juego
        if text == "/start":
            # Elige una pregunta aleatoria
            question = random.choice(questions)
            question_text = question["question"]
            answers = question["answers"]

            # Envía la pregunta con botones
            keyboard = {
                "inline_keyboard": [create_buttons(answers)]
            }

            # Enviar pregunta al chat
            requests.post(TELEGRAM_API, data={
                "chat_id": chat_id,
                "text": question_text,
                "reply_markup": str(keyboard)
            })

        # Si es una respuesta a una pregunta
        elif "callback_query" in update:
            callback_data = update["callback_query"]["data"]
            correct_answer = next(q["correct"] for q in questions if q["question"] == update["callback_query"]["message"]["text"])

            # Verifica si la respuesta es correcta
            if callback_data == correct_answer:
                response = "¡Correcto! 🎉"
            else:
                response = "¡Incorrecto! 😞"

            # Responde con el resultado
            requests.post(TELEGRAM_API, data={
                "chat_id": chat_id,
                "text": response
            })

    return "OK", 200

@app.route('/')
def index():
    return "🤖 ¡El bot de preguntas está funcionando!"

if __name__ == "__main__":
    app.run(debug=True)




