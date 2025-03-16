import requests
from bs4 import BeautifulSoup
from telebot import TeleBot, types
import random
import time
from flask import Flask
import os
import threading
import json

app = Flask(__name__)

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI"
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# User Data Storage
user_data = {}

# Save UID data to file
def save_user_data():
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)

# Load UID data from file
def load_user_data():
    global user_data
    try:
        with open("user_data.json", "r") as file:
            user_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = {}

# Load data at the start
load_user_data()

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
                 "🚀 *Flyjet Aviator Bot is Active!* \n"
                 "Send `/setuid <Your_UID>` to start receiving signals.", 
                 parse_mode='Markdown')

# /setuid command
@bot.message_handler(commands=['setuid'])
def set_uid(message):
    try:
        uid = message.text.split()[1].strip()
        user_data[message.chat.id] = uid
        save_user_data()  # Save UID to file
        bot.reply_to(message, f"✅ UID set successfully!\nNow you'll receive signals for UID: {uid}")
    except IndexError:
        bot.reply_to(message, "❗ Please provide a valid UID.\nExample: `/setuid 123456789`")

# Crash Point Scraper
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
        print(f"❌ Error for UID {uid}: {e}")
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
        for chat_id, uid in user_data.items():
            try:
                latest_crash_point = get_crash_point(uid)
                if latest_crash_point:
                    if uid not in crash_history:
                        crash_history[uid] = []
                    crash_history[uid].append(latest_crash_point)

                    if len(crash_history[uid]) >= 10:
                        signals = ""
                        for point in crash_history[uid][-10:]:
                            predicted_crash = predict_crash_point(crash_history[uid][-10:])
                            signals += f"💥 **Crash Point:** {point}x | 🧠 **Prediction:** {predicted_crash}x\n"

                        bot.send_message(chat_id, signals)
                else:
                    print(f"❗ Crash Point not found for UID {uid}")
                    
                time.sleep(10)
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(30)

# Flask Route for Render Port Issue Fix
@app.route('/')
def home():
    return "Flyjet Aviator Bot is Running!"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()  # Web scraping parallel run karega
    threading.Thread(target=bot.polling, kwargs={'none_stop': True}).start()  # Telegram bot commands ko handle karega
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
