import websocket
import json
import threading
from telebot import TeleBot, types
from flask import Flask, request
import os
import requests

app = Flask(__name__)

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI")
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# User data storage for UID mapping
user_data = {}

# WebSocket URL
WEBSOCKET_URL = "wss://game9.apac.spribegaming.com/BlueBox/websocket"

# Command Handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "🚀 *Flyjet Aviator Bot is Active!*\n"
        "Send `/setuid <Your_UID>` to start receiving signals.",
        parse_mode='Markdown'
    )

# Set UID Command
@bot.message_handler(commands=['setuid'])
def set_uid(message):
    try:
        uid = message.text.split()[1]
        user_data[message.chat.id] = uid
        bot.send_message(
            message.chat.id,
            f"✅ UID set successfully!\nNow you'll receive signals for UID: `{uid}`",
            parse_mode='Markdown'
        )
    except IndexError:
        bot.send_message(message.chat.id, "❗ Please provide a valid UID. Example: `/setuid 123456`", parse_mode='Markdown')

# WebSocket Data Handler
def on_message(ws, message):
    try:
        data = json.loads(message)
        if 'crashPoint' in data:
            crash_point = float(data['crashPoint'])
            send_signals_to_users(crash_point)
    except Exception as e:
        print(f"❌ Error in WebSocket message processing: {e}")

def on_error(ws, error):
    print(f"❗ WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 WebSocket Closed. Reconnecting in 5 seconds...")
    threading.Timer(5, connect_websocket).start()

def on_open(ws):
    print("✅ WebSocket Connected Successfully!")

# Send Signals to All Users
def send_signals_to_users(crash_point):
    for chat_id in user_data.keys():
        predicted_crash = round(crash_point * 1.3, 2)  # Example prediction logic
        bot.send_message(
            chat_id,
            f"💥 **Crash Point:** {crash_point}x | 🧠 **Prediction:** {predicted_crash}x",
            parse_mode='Markdown'
        )

# WebSocket Connection
def connect_websocket():
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()

# Flask Route for Webhook
@app.route('/' + TELEGRAM_BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "Success", 200

# Webhook Setup
@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    webhook_url = f"https://flyjet-aviator.onrender.com/{TELEGRAM_BOT_TOKEN}"
    if bot.set_webhook(url=webhook_url):
        return f"✅ Webhook set successfully at {webhook_url}"
    else:
        return "❌ Webhook setup failed", 400

# Home Route
@app.route('/')
def home():
    return "Flyjet Aviator Bot is Running!"

if __name__ == "__main__":
    # Delete Old Webhook Before Starting New One
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook")

    # Start WebSocket Thread
    threading.Thread(target=connect_websocket).start()

    # Start Flask App
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
