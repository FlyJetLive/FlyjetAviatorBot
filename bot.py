import websocket
import json
import random
from flask import Flask, request
from telebot import TeleBot
import threading
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI"
CHAT_ID = -4669657171

bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Crash History Data (From Screenshot)
crash_history = [
    2.39, 1.72, 6.61, 2.59, 1.19, 1.87, 1.09, 2.82, 1.39,
    2.45, 1.83, 5.02, 2.88, 2.02, 1.31, 1.31, 1.49, 2.74,
    1.18, 1.41, 8.63, 1.23, 4.80, 4.32, 1.63, 1.57
]

# ================= Crash Point Prediction Logic ================= #
def predict_crash_point(history):
    avg_crash_point = sum(history) / len(history)
    prediction = round(random.uniform(avg_crash_point * 0.8, avg_crash_point * 1.5), 2)
    return prediction

# ================= WebSocket Data Handler ================= #
def on_message(ws, message):
    try:
        data = json.loads(message)
        print("Received Data:", data)

        if 'crash_point' in data:
            crash_point = float(data['crash_point'])
            crash_history.append(crash_point)

            predicted_crash_point = predict_crash_point(crash_history[-20:])

            bot.send_message(
                CHAT_ID,
                f"💥 **Crash Point:** {crash_point}x\n"
                f"🧠 **Next Prediction:** {predicted_crash_point}x"
            )
    except Exception as e:
        print(f"❌ Error in Data Handling: {e}")

def on_error(ws, error):
    print(f"❌ WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 WebSocket Closed - Reconnecting...")
    start_websocket()

def on_open(ws):
    print("✅ WebSocket Connection Established")

# ================= Start WebSocket ================= #
def start_websocket():
    ws_url = "wss://game9.apac.spribegaming.com/BlueBox/websocket"
    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()

# ================= Flask Routes ================= #
@app.route('/')
def home():
    return "Flyjet Aviator Bot is Running!"

@app.route('/aviator', methods=['POST'])
def aviator_webhook():
    try:
        data = request.get_json(silent=True)
        print("Received Data:", data)  # ✅ Debugging ke liye data print karega

        if not data:
            return "❗ No data received or invalid format", 400
        
        signal = data.get('signal')
        predicted_crash_point = predict_crash_point(crash_history[-20:])

        if signal:
            bot.send_message(
                CHAT_ID,
                f"📊 **Aviator Signal Alert:** {signal}\n💥 **Crash Point Prediction:** {predicted_crash_point}x"
            )
            return "✅ Signal Sent Successfully", 200
        else:
            return "❗ No Signal Found", 400

    except Exception as e:
        print(f"❌ Error: {e}")
        return "❌ Internal Server Error", 500

# ================= Start WebSocket in Background ================= #
if __name__ == "__main__":
    threading.Thread(target=start_websocket).start()  # WebSocket parallel run hoga
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
