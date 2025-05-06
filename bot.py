from flask import Flask, request
import requests

app = Flask(__name__)

# TOKEN DE TELEGRAM (reemplázalo por tu token real)
TELEGRAM_TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Base de datos temporal en memoria
user_state = {}

# Lecciones y preguntas
lessons = [
    {
        "title": "Clase 1: ¿Qué es Python?",
        "content": "Python es un lenguaje de programación de alto nivel, interpretado y de propósito general. Es famoso por su sintaxis simple y legibilidad.",
        "question": {
            "text": "¿Qué tipo de lenguaje es Python?",
            "options": ["Compilado", "Interpretado", "Ensamblador"],
            "correct": "Interpretado"
        }
    },
    {
        "title": "Clase 2: Variables y Tipos de Datos",
        "content": "En Python, puedes crear variables sin declarar su tipo. Ejemplo: `nombre = 'Juan'` o `edad = 30`.",
        "question": {
            "text": "¿Qué tipo de dato es `True` en Python?",
            "options": ["String", "Booleano", "Entero"],
            "correct": "Booleano"
        }
    },
    # Puedes seguir agregando más clases aquí
]

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{TELEGRAM_API}/sendMessage", json=data)

def create_buttons(options):
    return [[{"text": opt, "callback_data": opt}] for opt in options]

def send_lesson(chat_id, index):
    if index >= len(lessons):
        send_message(chat_id, "🎉 ¡Felicidades! Has completado todas las clases.")
        return
    lesson = lessons[index]
    user_state[chat_id] = {"lesson": index}
    send_message(chat_id, f"{lesson['title']}\n\n{lesson['content']}")
    question = lesson["question"]
    keyboard = {"inline_keyboard": create_buttons(question["options"])}
    send_message(chat_id, f"🧠 Pregunta: {question['text']}", reply_markup=keyboard)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "👨‍🏫 ¡Bienvenido al curso de Python básico!")
            send_lesson(chat_id, 0)

    elif "callback_query" in update:
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        data = query["data"]
        state = user_state.get(chat_id, {})
        lesson_index = state.get("lesson", 0)
        lesson = lessons[lesson_index]
        correct_answer = lesson["question"]["correct"]

        if data == correct_answer:
            send_message(chat_id, "✅ ¡Correcto! Pasando a la siguiente lección...")
            send_lesson(chat_id, lesson_index + 1)
        else:
            send_message(chat_id, f"❌ Incorrecto. La respuesta correcta era: {correct_answer}")
            send_message(chat_id, "🧠 Vamos a repetir la lección.")
            send_lesson(chat_id, lesson_index)

    return "OK", 200

@app.route('/')
def index():
    return "🤖 El bot profesor de Python está activo"





