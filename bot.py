from flask import Flask, request
import requests
 
app = Flask(__name__)
 
TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()
 
    # Guardar log (similar a log.txt)
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(str(update) + '\n')
 
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        message = update["message"].get("text", "").lower()
 
        # Respuesta por defecto
        respuesta = "No entendí eso 🤔. Escribe /start para comenzar."
 
        # Respuestas más naturales y amigables
        if message == "/start":
            respuesta = (
                "¡Hola! 👋 Soy MacroB Bot 🤖.\n"
                "Estoy aquí para ayudarte. Puedes decirme cosas como:\n"
                "• hola\n"
                "• gracias\n"
                "• ¿quién eres?\n"
                "Y te responderé 😉"
            )
        elif message == "hola":
            respuesta = "¡Hola! 😄 ¿En qué puedo ayudarte hoy?"
        elif "gracias" in message:
            respuesta = "¡De nada! Estoy para ayudarte 😊"
        elif "quién eres" in message or "quien eres" in message:
            respuesta = "Soy MacroB Bot, un bot en desarrollo 🛠️. ¡Pero ya puedo conversar contigo!"
 
        # Enviar respuesta a Telegram
        requests.get(TELEGRAM_API_URL, params={
            "chat_id": chat_id,
            "text": respuesta
        })
 
    return "OK", 200
 
# Ruta para revisar log desde navegador
@app.route('/log', methods=['GET'])
def ver_log():
    try:
        with open('log.txt', 'r', encoding='utf-8') as file:
            return "<pre>" + file.read() + "</pre>"
    except FileNotFoundError:
        return "No hay log aún."
 
# Solo usado si corres localmente (en Render, se usa gunicorn)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
 
