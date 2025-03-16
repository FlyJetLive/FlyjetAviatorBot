from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

# Telegram Bot Token
BOT_TOKEN = "8162063342:AAGxQN9hq_M5xTvuRcBt0ONtqCZLkgbXeBI"  # <-- Yaha apna token daalo

# Sample round history (example data)
round_history = [4.31, 5.34, 1.13, 1.35, 1.14, 4.42, 589.99, 1.05, 1.17, 2.05, 1.00, 1.01, 1.00, 1.24, 6.19, 2.75]

# Function to generate signals
def generate_signals():
    signals = []
    for _ in range(10):
        avg = sum(round_history[-10:]) / len(round_history[-10:])
        min_multiplier = max(1.5, avg - random.uniform(0.5, 1.0))
        max_multiplier = min(8.0, avg + random.uniform(0.5, 2.0))
        signals.append(f"🎯 Bet between {min_multiplier:.2f}x - {max_multiplier:.2f}x")
    return signals

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Aviator Signals Bot! Type /signals to get 10 signals.")

# /signals command
async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sigs = generate_signals()
    message = "📡 *Aviator Signals* 📡\n\n" + "\n".join([f"{i+1}. {sig}" for i, sig in enumerate(sigs)])
    await update.message.reply_markdown(message)

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signals", signals))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
