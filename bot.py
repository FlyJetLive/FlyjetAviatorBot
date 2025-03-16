import requests
from bs4 import BeautifulSoup
from telebot import TeleBot
import random
import time
from flask import Flask
import os
import threading

app = Flask(__name__)

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI"
CHAT_ID = -4669657171
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Scraping Function
def get_crash_point():
    try:
        url = "https://aviator-next.spribegaming.com/?user=10500014800067&token=31333133325F6D..."
        headers = {"User-Agent": "Mozilla/5.0"}  # Avoid bot detection
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❗ Error: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        crash_point_element = soup.find('div', class_='crash-point')  
        if crash_point_element:
            crash_point = float(crash_point_element.text.strip().replace('x', ''))
            return crash_point
        else:
            print("❗ Crash Point Not Found - Selector Issue")
            return None
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return None

# Prediction Logic
def predict_crash_point(history):
    if len(history) < 5:
        return round(random.uniform(1.5, 3.0), 2)  # Random fallback for short history
    avg_point = sum(history) / len(history)
    return round(random.uniform(avg_point * 0.8, avg_point * 1.5), 2)

# Main Signal Logic
def run_bot():
    crash_history = []

    while True:
        try:
            latest_crash_point = get_crash_point()
            if latest_crash_point:
                crash_history.append(latest_crash_point)
                predicted_crash = predict_crash_point(crash_history[-10:])  # Last 10 points for prediction
                
                bot.send_message(
                    CHAT_ID,
                    f"💥 **Crash Point:** {latest_crash_point}x\n"
                    f"🧠 **Next Prediction:** {predicted_crash}x"
                )
            else:
                print("❗ Crash Point not found")
            
            time.sleep(10)  # Every 10 seconds check for updates
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(30)  # Wait longer if error occurs

# Flask Route for Render Port Issue Fix
@app.route('/')
def home():
    return "Flyjet Aviator Bot is Running!"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()  # Web scraping parallel run karega
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

