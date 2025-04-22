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
 
        respuesta = "No entendí eso. Escribe /start para comenzar."
 
        if message == "/start":
            respuesta = "¡Hola! 👋 Bienvenido a Macro3137 Bot 🤖. Escribe 'hola' o hazme una pregunta."
        elif message == "hola":
            respuesta = "¡Hola! ¿Cómo estás hoy?"
        elif "gracias" in message:
            respuesta = "¡De nada! 😊"
 
        requests.get(TELEGRAM_API_URL, params={
            "chat_id": chat_id,
            "text": respuesta
        })
 
    return "OK", 200
 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)