import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from llm import ChatGPT

# Load the API token from the environment variable
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
chatgpt = ChatGPT()

# Password requirement
REQUIRED_PASSWORD = "ZoomLink613!"

# Approved users list
APPROVED_USERS_FILE = "approved_users.txt"


# Load approved users from a file
def load_approved_users():
    if os.path.exists(APPROVED_USERS_FILE):
        with open(APPROVED_USERS_FILE, 'r') as file:
            return set(line.strip() for line in file)
    return set()


approved_users = load_approved_users()


# Save approved users to a file
def save_approved_users():
    with open(APPROVED_USERS_FILE, 'w') as file:
        for user_id in approved_users:
            file.write(f"{user_id}\n")


# Check if user is approved before handling other commands
def is_user_approved(update: Update) -> bool:
    user_id = str(update.message.from_user.id)
    return user_id in approved_users


# Handle user approval via password
async def handle_password(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    password = update.message.text.strip()

    if password == REQUIRED_PASSWORD:
        approved_users.add(user_id)
        save_approved_users()
        await update.message.reply_text("Password accepted! You are now approved to use the bot.")
        context.user_data['awaiting_password'] = False
    else:
        await update.message.reply_text("Incorrect password. Please try again.")
        context.user_data['awaiting_password'] = True


# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    if not is_user_approved(update):
        await update.message.reply_text("Please enter the password to use this bot:")
        context.user_data['awaiting_password'] = True
    else:
        await update.message.reply_text(
            'Hello! I am your ZoomLinkBot. Send me an image of a Zoom invite to extract the meeting link.')


# Handle image messages
async def handle_image(update: Update, context: CallbackContext) -> None:
    if not is_user_approved(update):
        await update.message.reply_text("You need to enter the password before using this bot. Use /start to begin.")
        return

    print("Received an image.")
    if update.message.photo:
        # Get the largest image file (highest resolution)
        file = await update.message.photo[-1].get_file()
        image_url = file.file_path
        print(f"Image URL: {image_url}")

        # Use ChatGPT to extract the Zoom link information
        try:
            zoom_info = chatgpt.extract_zoom_info(image_url)
            print(f"Extracted Zoom Info: {zoom_info}")

            # Create the response message with the plain text link
            response_message = (
                f"Meeting ID: {zoom_info.meeting_id}\n"
                f"Passcode: {zoom_info.passcode}\n"
                f"Join Zoom Meeting: {zoom_info.join_url}"
            )
            print(f"Response Message: {response_message}")
        except Exception as e:
            response_message = f"Could not extract Zoom information. Error: {str(e)}"
            print(response_message)

        # Send the extracted info back to the user
        await update.message.reply_text(response_message)


# Handle text messages (password entry)
async def handle_text(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_password', False):
        await handle_password(update, context)
    else:
        if not is_user_approved(update):
            await update.message.reply_text("Please enter the password to use this bot:")
            context.user_data['awaiting_password'] = True
        else:
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
