from websocket_handler import connect_websocket
from telebot import TeleBot, types
from flask import Flask, request
import os
import threading

app = Flask(__name__)

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI")
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# User Data
user_data = {}

# Signal Sending Logic
def send_signals_to_users(crash_point):
    for chat_id in user_data.keys():
        predicted_crash = round(crash_point * 1.3, 2)  # Example prediction logic
        bot.send_message(
            chat_id,
            f"💥 **Crash Point:** {crash_point}x | 🧠 **Prediction:** {predicted_crash}x",
            parse_mode='Markdown'
        )

# Command Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "🚀 *Flyjet Aviator Bot is Active!*\n"
        "Send `/setuid <Your_UID>` to start receiving signals.",
        parse_mode='Markdown'
    )

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


@app.route(f'/{os.getenv("TELEGRAM_BOT_TOKEN")}', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "OK", 200

# Webhook Setup
@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    webhook_url = f"https://flyjet-aviator.onrender.com/{TELEGRAM_BOT_TOKEN}"
    if bot.set_webhook(url=webhook_url):
        return f"✅ Webhook set successfully at {webhook_url}"
    else:
        return "❌ Webhook setup failed", 400

@app.route('/')
def home():
    return "Flyjet Aviator Bot is Running!"

if __name__ == "__main__":
    print("Bot Token:", TELEGRAM_BOT_TOKEN)  # Is line ko temporarily add karo
    
    # Delete Old Webhook Before Starting New One
    import requests
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook")

    # Start WebSocket in Thread
    threading.Thread(target=lambda: connect_websocket(send_signals_to_users)).start()

    # Start Flask App
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
