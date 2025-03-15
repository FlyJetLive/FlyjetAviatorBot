import asyncio
import websockets
import json
import os
from flask import Flask, request
from telegram import Bot

# Flask App for Render Deployment
app = Flask(__name__)

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI")
CHAT_ID = os.getenv("1002680639378")

bot = Bot(token=BOT_TOKEN)

# WebSocket URL for Aviator Game
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

                # Example data extraction (modify as per data format)
                if 'crash_point' in data:
                    crash_point = data['crash_point']

                    # Add signal to the list
                    signals.append(f"{crash_point}x")

                    # Send signal when 10 predictions are ready
                    if len(signals) == 10:
                        signal_text = "\n".join(signals)
                        await bot.send_message(CHAT_ID, f"🚨 **Aviator Signals** 🚨\n{signal_text}")
                        signals.clear()  # Clear the list for new predictions

            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(5)  # Retry after 5 seconds

@app.route('/aviator', methods=['POST'])
def manual_signal():
    try:
        data = request.json
        signal = data.get('signal', 'No Signal')
        bot.send_message(CHAT_ID, f"📊 **Manual Signal:** {signal}")
        return "Success", 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return "Error", 500

# Start the WebSocket connection
async def main():
    await aviator_signal()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
