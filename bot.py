import requests
from bs4 import BeautifulSoup
from telebot import TeleBot
import random
import time

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI"
CHAT_ID = -4669657171
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Scraping Function
def get_crash_point():
    url = "https://aviator-next.spribegaming.com/?user=10500014800067&token=31333133325F6D..."
    headers = {"User-Agent": "Mozilla/5.0"}  # Avoid bot detection
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Crash Point Extraction (Selector needs adjustment as per HTML structure)
    crash_point_element = soup.find('div', class_='crash-point')
    if crash_point_element:
        crash_point = float(crash_point_element.text.strip().replace('x', ''))
        return crash_point
    return None

# Prediction Logic
def predict_crash_point(history):
    if len(history) < 5:
        return round(random.uniform(1.5, 3.0), 2)  # Random fallback for short history
    avg_point = sum(history) / len(history)
    return round(random.uniform(avg_point * 0.8, avg_point * 1.5), 2)

# Main Signal Logic
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
