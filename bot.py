import telebot
from flask import Flask, request
import os
import logging
from logging import handlers
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Use environment variables for token and webhook URL
TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot Token
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Full webhook URL, e.g., https://your-app.koyeb.app/<BOT_TOKEN>

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    start_text = (
        "Hello! I am your menu bot.\n\n"
        "➤ Click the buttons below to access various channels or explore more options.\n"
        "➤ You can always return to the main menu by clicking 'Back'."
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Go to Channel 1", url="https://t.me/yourchannel1"))
    markup.add(InlineKeyboardButton("Go to Channel 2", url="https://t.me/yourchannel2"))
    markup.add(InlineKeyboardButton("More Options", callback_data="more_options"))
    bot.send_message(message.chat.id, start_text, reply_markup=markup)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ More options ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "more_options":
        more_options_text = "Here are more channels you might like:\n"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Channel 3", url="https://t.me/yourchannel3"))
        markup.add(InlineKeyboardButton("Channel 4", url="https://t.me/yourchannel4"))
        markup.add(InlineKeyboardButton("Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text(
            more_options_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup
        )
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main menu ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
    elif call.data == "main_menu":
        start_text = (
            "Hello! I am your menu bot.\n\n"
            "➤ Click the buttons below to access various channels or explore more options.\n"
            "➤ You can always return to the main menu by clicking 'Back'."
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Go to Channel 1", url="https://t.me/yourchannel1"))
        markup.add(InlineKeyboardButton("Go to Channel 2", url="https://t.me/yourchannel2"))
        markup.add(InlineKeyboardButton("More Options", callback_data="more_options"))
        bot.edit_message_text(
            start_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup
        )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Webhook & Health check ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = handlers.RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Validate environment variables
if not TOKEN or not WEBHOOK_URL:
    logger.error("BOT_TOKEN and/or WEBHOOK_URL environment variables are missing.")
    raise EnvironmentError("BOT_TOKEN and/or WEBHOOK_URL environment variables are not set.")

# Health check route for Koyeb
@app.route("/health", methods=["GET"])
def health_check():
    try:
        return "OK", 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return "Error", 500

# Webhook route to handle updates from Telegram
def set_webhook():
    webhook_url = os.getenv("WEBHOOK_URL")  # Your Koyeb app's public URL
    if not webhook_url:
        raise ValueError("WEBHOOK_URL is not set in environment variables.")
    
    url = f"{TELEGRAM_API_URL}/setWebhook"
    data = {"url": webhook_url}
    response = requests.post(url, data=data)
    
    if response.status_code != 200:
        raise RuntimeError(f"Failed to set webhook: {response.text}")
    return response.json()

@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

if __name__ == "__main__":
    # Set webhook when the script starts
    logger.info("Setting webhook...")
    result = set_webhook()
    logger.info(f"Webhook set: {result}")
    app.run(host="0.0.0.0", port=5000)
