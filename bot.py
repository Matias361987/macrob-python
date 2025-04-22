from flask import Flask, request
import requests
 
app = Flask(__name__)
 
# Tu token real
TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
# Webhook principal
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
 
    if not update or 'message' not in update:
        return "No content", 200
 
    chat_id = update['message']['chat']['id']
    message = update['message'].get('text', '').lower()
 
    # Lógica de respuesta
    respuesta = "No entendí 🤔. Escribe /start para comenzar."
 
    if message == '/start':
        respuesta = "👋 ¡Hola! Soy MacroB Bot. Escribe 'hola', 'gracias', o 'quién eres'."
    elif message == 'hola':
        respuesta = "¡Hola! 😄 ¿Cómo estás?"
    elif 'gracias' in message:
        respuesta = "¡De nada! 🙌"
    elif 'quién eres' in message or 'quien eres' in message:
        respuesta = "Soy MacroB Bot, tu asistente virtual en desarrollo 🚀"
 
    # Enviar respuesta
    requests.get(TELEGRAM_URL, params={
        'chat_id': chat_id,
        'text': respuesta
    })
 
    return "OK", 200
 
# Ruta para test (opcional)
@app.route('/', methods=['GET'])
def index():
    return "✅ Bot en línea"
