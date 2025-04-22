from flask import Flask, request
 
app = Flask(__name__)
 
@app.route('/', methods=['POST'])
def webhook():
    print("📥 Webhook POST recibido")
    return "OK", 200
 
@app.route('/', methods=['GET'])
def index():
    return "🏠 Bot activo", 200
