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

        # 🚨 Proper Signal Alerts Logic
        if signal == 'BUY':
            bot.send_message(CHAT_ID, "**Upstox Signal Alert:** 📈 Buy Signal")
        elif signal == 'SELL':
            bot.send_message(CHAT_ID, "**Upstox Signal Alert:** 📉 Sell Signal")
        else:
            bot.send_message(CHAT_ID, "**Upstox Signal Alert:** 🚫 No Signal")
    
    return "Success", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
