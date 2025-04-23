from flask import Flask, request
import requests
import random

app = Flask(__name__)

# Token de Telegram
TELEGRAM_TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# Lista de preguntas y respuestas
quiz = [
    {"question": "¿Cuál es la capital de Francia?", "answer": "parís"},
    {"question": "¿Quién escribió 'Don Quijote de la Mancha'?", "answer": "miguel de cervantes"},
    {"question": "¿En qué año llegó el hombre a la luna?", "answer": "1969"},
    {"question": "¿Cuántos continentes hay en el mundo?", "answer": "7"},
    {"question": "¿Qué es la fotosíntesis?", "answer": "proceso en el que las plantas convierten la luz en energía"}
]

# Enviar mensaje a Telegram
def send_message(chat_id, text):
    requests.get(TELEGRAM_API, params={
        "chat_id": chat_id,
        "text": text
    })

# Función para manejar el webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()

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



