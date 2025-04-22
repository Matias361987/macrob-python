from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])  # Cambiado a POST
def webhook():
    update = request.get_json()

    with open("log.txt", "a", encoding="utf-8") as f:
        f.write("📥 Update:\n" + str(update) + "\n\n")

    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "").lower()

        # Lógica para responder automáticamente según el mensaje
        if 'hola' in text:
            reply = "¡Hola! ¿Cómo puedo ayudarte hoy? 🤖"
        elif 'ayuda' in text:
            reply = "¡Claro! Puedo responder tus preguntas. ¿Qué necesitas saber?"
        elif 'adiós' in text:
            reply = "¡Hasta luego! ¡Que tengas un buen día! 👋"
        else:
            reply = "✅ Recibido: " + text

        # Enviar respuesta
        requests.get(TELEGRAM_API, params={
            "chat_id": chat_id,
            "text": reply
        })

    return "OK", 200

@app.route('/')
def index():
    return "🤖 MacroBot está vivo"

@app.route('/log')
def log():
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            return "<pre>" + f.read() + "</pre>"
    except:
        return "Sin logs aún."

