# main.py
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from llm import ChatGPT

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

        # Use ChatGPT to extract and parse the Zoom link information
        try:
            zoom_info_text = chatgpt.extract_zoom_info(image_url)
            zoom_info = chatgpt.parse_zoom_info(zoom_info_text)

            # Create a clickable Zoom link
            clickable_link = f"[Join Zoom Meeting]({zoom_info.join_url})"
            response_message = (
                f"Meeting ID: {zoom_info.meeting_id}\n"
                f"Passcode: {zoom_info.passcode}\n"
                f"{clickable_link}"
            )
        except Exception as e:
            response_message = f"Could not extract Zoom information. Error: {str(e)}"

        # Send the extracted info back to the user
        await update.message.reply_text(response_message, parse_mode="Markdown")

async def handle_text(update: Update, context: CallbackContext) -> None:
    # Do nothing for text messages without images
    await update.message.reply_text("Please send an image of a Zoom invite.")

def main():
    application = Application.builder().token(API_TOKEN).build()

    # Start command handler
    application.add_handler(CommandHandler('start', start))

    # Image message handler
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Text message handler (for messages without images)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
