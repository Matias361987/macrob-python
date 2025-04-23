from flask import Flask, request
import requests
import openai

app = Flask(__name__)

# Token de Telegram
TELEGRAM_TOKEN = '7510833304:AAEDIrWS_27AhGxHAnuzvJx3XxXRclhZFuI'
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# Token de OpenAI (REEMPLAZA ESTO CON TU TOKEN REAL)
openai.api_key = "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"

@app.route('/')
def home():
    return "🤖 MacroBot + ChatGPT activo"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Obtener respuesta desde ChatGPT
        respuesta = chatgpt(text)

        # Enviar respuesta a Telegram
        requests.post(TELEGRAM_API, json={
            "chat_id": chat_id,
            "text": respuesta
        })

    return "OK", 200

def chatgpt(pregunta):
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil y simpático."},
                {"role": "user", "content": pregunta}
            ]
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error al consultar ChatGPT: {e}"



