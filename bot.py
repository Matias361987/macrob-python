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
            correct_answer = questions[0]["correct"]

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
    return "🤖 MacroBot está vivo"

if __name__ == '__main__':
    app.run(debug=True)

    # Obtenemos el chat_id y el mensaje
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "").lower()

        if text == "/start":
            # Saludo inicial y pregunta inicial
            send_message(chat_id, "¡Hola! Soy tu bot de quiz. ¿Listo para comenzar?")
            send_message(chat_id, "Responde a la siguiente pregunta:")

            # Elegimos una pregunta aleatoria
            question = random.choice(quiz)
            send_message(chat_id, question["question"])

            # Guardamos la respuesta correcta en el chat_id
            # (Lo harías mejor con una base de datos, pero lo simplificamos aquí)
            send_message(chat_id, f"Respuesta correcta: {question['answer']}")

        elif text in [item["answer"] for item in quiz]:
            send_message(chat_id, "¡Correcto! Bien hecho.")
        else:
            send_message(chat_id, "Lo siento, la respuesta es incorrecta. Inténtalo de nuevo.")

    return "OK", 200

@app.route('/')
def index():
    return "🤖 ¡El bot de preguntas está funcionando!"

if __name__ == "__main__":
    app.run(debug=True)



