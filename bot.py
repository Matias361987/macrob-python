from flask import Flask, request
import requests
 
app = Flask(__name__)
 
TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
 
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
 
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write("📥 RECIBIDO:\n")
        f.write(str(update) + "\n\n")
 
    if not update or "message" not in update:
        return "No data", 200
 
    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "").lower()
 
    # Respuesta mínima
    respuesta = f"Recibí: {text}"
 
    # Enviar mensaje a Telegram
    r = requests.get(TELEGRAM_URL, params={
        "chat_id": chat_id,
        "text": respuesta
    })
 
    print("📤 Enviado a Telegram:", r.status_code)
    return "OK", 200
 
@app.route('/', methods=['GET'])
def index():
    return "✅ Bot corriendo"
 
@app.route('/log', methods=['GET'])
def ver_log():
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            return "<pre>" + f.read() + "</pre>"
    except:
        return "Sin logs"
