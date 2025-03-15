import os
import asyncio
import websockets
import json
from flask import Flask, request
from telebot import TeleBot

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI")
CHAT_ID = os.getenv("1002680639378")

bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Flask App Setup
app = Flask(__name__)

# WebSocket URL (Aviator API URL)
WS_URL = "wss://game9.apac.spribegaming.com/BlueBox/websocket"

# Signal Prediction Logic
async def aviator_signal():
    async with websockets.connect(WS_URL) as ws:
        print("✅ Connected to WebSocket")

        signals = []  # List to store 10 signals

        while True:
            try:
                message = await ws.recv()
                data = json.loads(message)

                # Example data extraction (Modify as per data format)
                if 'crash_point' in data:
                    crash_point = data['crash_point']

                    # Add signal to the list
                    signals.append(f"{crash_point}x")

                    # Send signal when 10 predictions are ready
                    if len(signals) == 10:
                        signal_text = "\n".join(signals)
                        bot.send_message(CHAT_ID, f"🚨 **Aviator Signals** 🚨\n{signal_text}")
                        signals.clear()  # Clear the list for new predictions

            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(5)  # Retry after 5 seconds

# Flask Route for Testing
@app.route('/')
def home():
    return "Flyjet Aviator Bot is Running!"

# Webhook Route for Testing Signals (Optional)
@app.route('/aviator', methods=['POST'])
def webhook():
    data = request.get_json()
    signal = data.get("signal", "No Signal")
    bot.send_message(CHAT_ID, f"📊 **Aviator Signal Alert:** {signal}")
    return "Signal Received", 200

# Start the WebSocket connection
async def main():
    await aviator_signal()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    asyncio.run(main())
    app.run(host='0.0.0.0', port=port, threaded=True)
