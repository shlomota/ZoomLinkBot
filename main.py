from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your API token from BotFather
API_TOKEN = 'YOUR_API_TOKEN'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your ZoomLinkBot. Send me "abc" to see me in action.')

def respond_to_abc(update: Update, context: CallbackContext) -> None:
    if 'abc' in update.message.text.lower():
        update.message.reply_text('ABC')

def main():
    updater = Updater(API_TOKEN)

    dispatcher = updater.dispatcher

    # Start command handler
    dispatcher.add_handler(CommandHandler('start', start))

    # Text message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond_to_abc))

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
