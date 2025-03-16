import requests
from bs4 import BeautifulSoup
from telebot import TeleBot, types
import random
import time
from flask import Flask
import os
import threading

app = Flask(__name__)

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI"
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Dictionary to Store User UIDs and Chat IDs
user_data = {}

# Base URL for Aviator
BASE_URL = "https://aviator-next.spribegaming.com/?user={}&token=YOUR_TOKEN_HERE&lang=en&currency=INR"

# /start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 *Flyjet Aviator Bot is Active!*\n\nSend `/setuid <Your_UID>` to start receiving signals.", parse_mode='Markdown')

# /setuid Command
@bot.message_handler(commands=['setuid'])
def set_uid(message):
    try:
        uid = message.text.split()[1]
        chat_id = message.chat.id
        user_data[chat_id] = uid
        bot.reply_to(message, f"✅ UID set successfully!\nNow you'll receive signals for UID: `{uid}`", parse_mode='Markdown')
    except IndexError:
        bot.reply_to(message, "❗ Please provide your UID like this:\n`/setuid 10500014800067`", parse_mode='Markdown')

# Scraping Function
def get_crash_point(uid):
    try:
        url = BASE_URL.format(uid)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, 'html.parser')
        crash_point_element = soup.find('div', class_='crash-point')

        if crash_point_element:
            crash_point = float(crash_point_element.text.strip().replace('x', ''))
            return crash_point
        else:
            return None
    except Exception as e:
        print(f"❌ Error during scraping for UID {uid}: {e}")
        return None

# Prediction Logic
def predict_crash_point(history):
    if len(history) < 3:
        return round(random.uniform(1.5, 3.0), 2)
    avg_point = sum(history) / len(history)
    return round(random.uniform(avg_point * 0.8, avg_point * 1.5), 2)

# Main Signal Logic
def run_bot():
    user_histories = {}

    while True:
        for chat_id, uid in user_data.items():
            if chat_id not in user_histories:
                user_histories[chat_id] = []

            latest_crash_point = get_crash_point(uid)
            if latest_crash_point:
                user_histories[chat_id].append(latest_crash_point)
                user_histories[chat_id] = user_histories[chat_id][-10:]

                signals = "📊 *Crash Point Predictions:*\n\n"
                for point in user_histories[chat_id]:
                    predicted_crash = predict_crash_point(user_histories[chat_id])
                    signals += f"💥 **Crash Point:** {point}x | 🧠 **Prediction:** {predicted_crash}x\n"

                bot.send_message(chat_id, signals, parse_mode='Markdown')

            time.sleep(5)

# Flask Route for Render Port Issue Fix
@app.route('/')
def home():
    return "Flyjet Aviator Bot is Running!"

if __name__ == "__main__":
    bot.remove_webhook()  # Forcefully webhook delete
    threading.Thread(target=run_bot, daemon=True).start()  
    threading.Thread(target=lambda: bot.infinity_polling()).start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
