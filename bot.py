from flask import Flask, request
import telebot
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '8046226594:AAHvoxw8pVdLoXGa9cDCnF-kfS5TBOmV_Fw'
CHAT_ID = '6536224568'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        signal = data.get('signal', 'No Signal')
        bot.send_message(CHAT_ID, f"📊 **Upstox Signal Alert:** {signal}")
    return "Success", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
