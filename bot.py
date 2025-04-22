from flask import Flask, request
import requests
 
app = Flask(__name__)
 
TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
 
@app.route('/', methods=['POST'])
def webhook():
    print("📥 Webhook recibido")
 
    update = request.get_json()
    print(f"📦 Contenido recibido: {update}")
 
    # Guardar log para Render Free
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write("📥 Webhook recibido\n")
        log_file.write(str(update) + '\n')
 
    if not update:
        print("⚠️ No se recibió un JSON válido")
        return "No JSON", 400
 
    if "message" not in update:
        print("⚠️ JSON recibido sin 'message'")
        return "No message", 200
 
    chat_id = update["message"]["chat"]["id"]
    message = update["message"].get("text", "").lower()
    print(f"💬 Mensaje recibido: {message}")
 
    respuesta = "No entendí eso 🤔. Escribe /start para comenzar."
 
    # Respuestas personalizadas
    if message == "/start":
        respuesta = (
            "¡Hola! 👋 Soy MacroB Bot 🤖.\n"
            "Estoy aquí para ayudarte. Puedes decirme cosas como:\n"
            "• hola\n"
            "• gracias\n"
            "• ¿quién eres?\n"
            "¡Y te responderé con gusto! 😉"
        )
    elif message == "hola":
        respuesta = "¡Hola! 😄 ¿En qué puedo ayudarte hoy?"
    elif "gracias" in message:
        respuesta = "¡De nada! Estoy para ayudarte 😊"
    elif "quién eres" in message or "quien eres" in message:
        respuesta = "Soy MacroB Bot, un bot en desarrollo 🛠️. ¡Pero ya puedo conversar contigo!"
 
    # Enviar mensaje
    try:
        response = requests.get(TELEGRAM_API_URL, params={
            "chat_id": chat_id,
            "text": respuesta
        })
        print(f"✅ Mensaje enviado. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
 
    return "OK", 200
 
# Ruta para ver logs desde navegador
@app.route('/log', methods=['GET'])
def ver_log():
    try:
        with open('log.txt', 'r', encoding='utf-8') as file:
            return "<pre>" + file.read() + "</pre>"
    except FileNotFoundError:
        return "No hay log aún."
 
# Test GET para confirmar que el servidor levanta
@app.route('/', methods=['GET'])
def index():
    return "✅ MacroB Bot está corriendo correctamente"
 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
