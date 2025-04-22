from flask import Flask, request

import requests
 
app = Flask(__name__)
 
TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
@app.route('/', methods=['POST'])

def webhook():

    update = request.get_json()
 
    # Guardar log para revisar

    with open('log.txt', 'a', encoding='utf-8') as log_file:

        log_file.write("📥 Webhook recibido:\n")

        log_file.write(str(update) + '\n\n')
 
    if not update or "message" not in update:

        return "No content", 200
 
    chat_id = update["message"]["chat"]["id"]

    message = update["message"].get("text", "").lower()
 
    respuesta = "No entendí eso 🤔. Escribe /start para comenzar."
 
    if message == "/start":

        respuesta = (

            "¡Hola! 👋 Soy MacroB Bot 🤖\n"

            "Puedes decirme cosas como:\n"

            "• hola\n"

            "• gracias\n"

            "• ¿quién eres?\n"

        )

    elif message == "hola":

        respuesta = "¡Hola! 😄 ¿Cómo estás?"

    elif "gracias" in message:

        respuesta = "¡De nada! Estoy feliz de ayudarte 😎"

    elif "quién eres" in message or "quien eres" in message:

        respuesta = "Soy MacroB Bot, tu asistente Telegram. 🚀"
 
    try:

        requests.get(TELEGRAM_API_URL, params={

            "chat_id": chat_id,

            "text": respuesta

        })

    except Exception as e:

        with open('log.txt', 'a', encoding='utf-8') as log_file:

            log_file.write(f"❌ Error al enviar mensaje: {e}\n")
 
    return "OK", 200
 
@app.route('/log', methods=['GET'])

def ver_log():

    try:

        with open('log.txt', 'r', encoding='utf-8') as file:

            return "<pre>" + file.read() + "</pre>"

    except FileNotFoundError:

        return "No hay log aún."
 
@app.route('/', methods=['GET'])

def index():

    return "✅ MacroB Bot Flask activo"

 
@app.route('/', methods=['GET'])
def index():
    return "✅ MacroB Bot está corriendo correctamente"
 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
