import os
import logging
import requests
from logging import handlers
from flask import Flask, request
import telebot
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
    return "OK", 200

# Webhook route to handle updates from Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Set webhook
def set_webhook():
    if not WEBHOOK_URL:
        raise ValueError("WEBHOOK_URL is not set in environment variables.")
    
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}
    response = requests.post(url, data=data)
    
    if response.status_code != 200:
        raise RuntimeError(f"Failed to set webhook: {response.text}")
    return response.json()

if __name__ == "__main__":
    # Set webhook when the script starts
    logger.info("Setting webhook...")
    result = set_webhook()
    logger.info(f"Webhook set: {result}")
    app.run(host="0.0.0.0", port=5000)
