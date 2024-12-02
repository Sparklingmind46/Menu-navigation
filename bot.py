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
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    try:
        json_data = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return "Internal Server Error", 500

# Set webhook on startup
@app.before_first_request
def set_webhook():
    try:
        bot.remove_webhook()  # Remove any existing webhook
        response = bot.set_webhook(url=WEBHOOK_URL)  # Set the new webhook with Koyeb URL
        if not response:
            logger.error("Failed to set webhook.")
        else:
            logger.info(f"Webhook set successfully: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Error setting webhook: {str(e)}")
        raise RuntimeError(f"Failed to set webhook: {str(e)}")

# Run the Flask app
if __name__ == "__main__":
    try:
        # Ensure the webhook is set before starting the app
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    except Exception as e:
        logger.error(f"Error starting Flask app: {str(e)}")
