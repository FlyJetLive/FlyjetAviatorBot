import asyncio
import websockets
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json

# Bot Token
BOT_TOKEN = "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI"

# Global Variable to store latest signal
latest_signal = "❌ No signal available yet. Please try later."

# WebSocket URL
WS_URL = "wss://game9.apac.spribegaming.com/BlueBox/websocket"

# Function to connect WebSocket and update latest_signal
async def websocket_listener():
    global latest_signal
    async with websockets.connect(WS_URL) as websocket:
        print("🟢 Connected to WebSocket")
        while True:
            try:
                message = await websocket.recv()
                print(f"📩 WebSocket Message: {message}")

                # Parse the WebSocket message here (Assuming JSON)
                data = json.loads(message)

                # Example: If crash point data is in `data['crashPoint']`
                if 'crashPoint' in data:
                    crash_point = data['crashPoint']
                    latest_signal = f"🚀 New Signal: Crash at {crash_point}x"

            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(5)  # Reconnect after delay

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Type /signals to get the latest Aviator signal!")

# /signals command
async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(latest_signal)

# Main Function to start bot and websocket
async def main():
    # Create bot app
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signals", signals))

    # Run WebSocket and bot polling together
    await asyncio.gather(
        websocket_listener(),  # Run websocket listener
        app.run_polling()      # Run bot polling
    )

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
