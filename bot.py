import requests
from bs4 import BeautifulSoup
from telebot import TeleBot
import time
import os

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI")
CHAT_ID = os.getenv("CHAT_ID", "-1002675709275")
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Aviator Signals URL
URL = "https://damangames.bet/aviator-signal-source"  # Example URL (change if required)

def get_crash_points():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    crash_points = []

    for div in soup.find_all('div', class_='crash-point-class'):  # Update class name accordingly
        try:
            point = float(div.text.strip().replace('x', ''))
            crash_points.append(point)
        except ValueError:
            continue

    return crash_points[:10]  # Send 10 rounds only

def send_signals():
    while True:
        crash_points = get_crash_points()
        if crash_points:
            signal_message = "\n".join([f"Round {i+1}: {point}x" for i, point in enumerate(crash_points)])
            bot.send_message(CHAT_ID, f"📊 *Flyjet Aviator Signals* \n{signal_message}", parse_mode='Markdown')
        else:
            bot.send_message(CHAT_ID, "❌ No crash points found at the moment.")

        time.sleep(10)  # Refresh interval (adjust if needed)

if __name__ == "__main__":
    bot.send_message(CHAT_ID, "✅ *Flyjet Aviator Bot Started!* Signals incoming...", parse_mode='Markdown')
    send_signals()
