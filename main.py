import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from chatgpt_module import ChatGPT

# Load the API token from the environment variable
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
chatgpt = ChatGPT()

if not API_TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am your ZoomLinkBot. Send me an image of a Zoom invite to extract the meeting link.')

async def handle_image(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        # Get the largest image file (highest resolution)
        file = await update.message.photo[-1].get_file()
        image_url = file.file_path

        # Use ChatGPT to extract the Zoom link information
        zoom_info = chatgpt.extract_zoom_info(image_url)

        # Send the extracted info back to the user
        await update.message.reply_text(f'Extracted Zoom Info:\n{zoom_info}')

def main():
    application = Application.builder().token(API_TOKEN).build()

    dispatcher = application.dispatcher

    # Start command handler
    dispatcher.add_handler(CommandHandler('start', start))

    # Image message handler
    dispatcher.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
