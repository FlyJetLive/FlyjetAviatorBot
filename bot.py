from flask import Flask, request
import telebot
import requests
import os
from upstox_api.api import Upstox, OrderType, TransactionType  # 👈 Upstox API Import

app = Flask(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = '8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI'
CHAT_ID = '-1002680639378'
UPSTOX_API_KEY = '89f0ab80-c2ed-4b19-99c1-6d42f6b1e668'
UPSTOX_API_SECRET = 'fvuqmloiwn'
UPSTOX_ACCESS_TOKEN = 'YOUR_UPSTOX_ACCESS_TOKEN'  # ⚠️ Yahan naye token dalna hai

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Upstox API Setup
u = Upstox(UPSTOX_API_KEY, UPSTOX_API_SECRET)
u.set_access_token(UPSTOX_ACCESS_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Example Signal Logic — Modify as needed
        signals = []
        symbols = ["NSE_EQ|RELIANCE", "NSE_EQ|TATASTEEL", "NSE_EQ|INFY"]

        for symbol in symbols:
            quote = u.get_live_feed(symbol, 'Full')
            ltp = quote['last_price']
            if ltp > 2500:  # Custom logic for signal generation
                signals.append({"symbol": symbol, "action": "BUY"})
            else:
                signals.append({"symbol": symbol, "action": "SELL"})

        # 📊 Signal Summary Create Karna
        message = "**📊 Upstox Signal Summary:**\n\n"
        for i, signal in enumerate(signals[:10], start=1):
            symbol = signal.get('symbol', 'Unknown')
            action = signal.get('action', 'No Signal')
            emoji = "📈" if action == "BUY" else "📉" if action == "SELL" else "❓"
            message += f"{i}. {symbol} ➔ {emoji} {action}\n"

        bot.send_message(CHAT_ID, message)
        return "Success", 200

    except Exception as e:
        print("Error:", e)
        bot.send_message(CHAT_ID, "❗ Error fetching signals.")
        return "Error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
