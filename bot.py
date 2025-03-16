import requests
from bs4 import BeautifulSoup
from telebot import TeleBot, types
import random
import time
from flask import Flask, request
import os
import threading

app = Flask(__name__)

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❗ TELEGRAM_BOT_TOKEN environment variable is missing!")

bot = TeleBot(TELEGRAM_BOT_TOKEN)

# User data storage for UID mapping
user_data = {}

# Command Handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
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
        bot.reply_to(
            message,
            f"✅ UID set successfully!\nNow you'll receive signals for UID: `{uid}`",
            parse_mode='Markdown'
        )
    except IndexError:
        bot.reply_to(message, "❗ Please provide a valid UID. Example: `/setuid 123456`", parse_mode='Markdown')

# Scraping Function
def get_crash_point(uid):
    try:
        url = f"https://aviator-next.spribegaming.com/?user={uid}&token=31333133325F6D..."
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, 'html.parser')
        crash_point_element = soup.find('div', class_='crash-point')

        if crash_point_element:
            crash_point = float(crash_point_element.text.strip().replace('x', ''))
            return crash_point
        else:
            print(f"❗ Crash Point Not Found for UID {uid}")
            return None
    except Exception as e:
        print(f"❌ Error during scraping for UID {uid}: {e}")
        return None

# Prediction Logic
def predict_crash_point(history):
    if len(history) < 5:
        return round(random.uniform(1.5, 3.0), 2)
    avg_point = sum(history) / len(history)
    return round(random.uniform(avg_point * 0.8, avg_point * 1.5), 2)

# Main Signal Logic
def run_bot():
    crash_history = {}

    while True:
        try:
            for chat_id, uid in user_data.items():
                if uid not in crash_history:
                    crash_history[uid] = []

                latest_crash_point = get_crash_point(uid)
                if latest_crash_point:
                    crash_history[uid].append(latest_crash_point)
                    if len(crash_history[uid]) >= 10:
                        signals = ""
                        for point in crash_history[uid][-10:]:
                            predicted_crash = predict_crash_point(crash_history[uid][-10:])
                            signals += f"💥 **Crash Point:** {point}x | 🧠 **Prediction:** {predicted_crash}x\n"

                        bot.send_message(chat_id, signals)
                else:
                    print(f"❗ No crash point found for UID {uid}")

            time.sleep(10)
        except Exception as e:
            print(f"❌ Error in bot loop: {e}")
            time.sleep(30)

# Flask Route for Render Port Issue Fix
@app.route('/')
def home():
    return "Flyjet Aviator Bot is Running!"

if __name__ == "__main__":
    # Webhook Reset to Avoid Conflict
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook")

    # Start threads
    threading.Thread(target=run_bot).start()
    threading.Thread(target=bot.polling, kwargs={'allowed_updates': types.Update.MESSAGE}).start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
