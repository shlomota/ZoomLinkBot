import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load the API token from the environment variable
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am your ZoomLinkBot. Send me "abc" to see me in action.')

async def respond_to_abc(update: Update, context: CallbackContext) -> None:
    if 'abc' in update.message.text.lower():
        await update.message.reply_text('ABC')

def main():
    application = Application.builder().token(API_TOKEN).build()

    # Start command handler
    application.add_handler(CommandHandler('start', start))

    # Text message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond_to_abc))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
