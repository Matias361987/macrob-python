from flask import Flask, request
import requests
import random

app = Flask(__name__)

# Token de Telegram
TELEGRAM_TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Lista de preguntas
questions = [
    {"question": "¿Cuál es la capital de Francia?", "answers": ["Madrid", "París", "Roma"], "correct": "París"},
    {"question": "¿En qué año llegó el hombre a la luna?", "answers": ["1965", "1969", "1972"], "correct": "1969"},
    {"question": "¿Cuál es el planeta más cercano al sol?", "answers": ["Mercurio", "Venus", "Tierra"], "correct": "Mercurio"},
    {"question": "¿Quién escribió 'Cien años de soledad'?", "answers": ["Borges", "García Márquez", "Cortázar"], "correct": "García Márquez"},
    {"question": "¿Cuántos lados tiene un hexágono?", "answers": ["5", "6", "8"], "correct": "6"},
    {"question": "¿Qué gas respiramos para vivir?", "answers": ["Dióxido de carbono", "Oxígeno", "Hidrógeno"], "correct": "Oxígeno"},
    {"question": "¿Cuál es el océano más grande?", "answers": ["Atlántico", "Índico", "Pacífico"], "correct": "Pacífico"},
]

# Guardamos preguntas por chat (temporalmente)
user_state = {}

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{TELEGRAM_API}/sendMessage", json=data)

def create_buttons(answers):
    return [[{"text": ans, "callback_data": ans}] for ans in answers]

def send_question(chat_id):
    question = random.choice(questions)
    user_state[chat_id] = question  # Guardamos la pregunta actual

    keyboard = {"inline_keyboard": create_buttons(question["answers"])}
    send_message(chat_id, question["question"], reply_markup=keyboard)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "¡Hola! Vamos a jugar una trivia 🎉")
            send_question(chat_id)

    elif "callback_query" in update:
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        answer = query["data"]

        correct = user_state.get(chat_id, {}).get("correct", "")
        if answer == correct:
            response = "¡Correcto! 🎉"
        else:
            response = f"¡Incorrecto! 😞 La respuesta era: {correct}"

        # Preguntar si quiere seguir
        followup_keyboard = {
            "inline_keyboard": [
                [{"text": "Sí", "callback_data": "jugar_otra"}],
                [{"text": "No", "callback_data": "fin"}]
            ]
        }

        send_message(chat_id, response)
        send_message(chat_id, "¿Quieres otra pregunta?", reply_markup=followup_keyboard)

    elif "callback_query" in update:
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        data = query["data"]

        if data == "jugar_otra":
            send_question(chat_id)
        elif data == "fin":
            send_message(chat_id, "¡Gracias por jugar! 👋")

    return "OK", 200

@app.route('/')
def index():
    return "🤖 ¡El bot de trivia está activo!"





