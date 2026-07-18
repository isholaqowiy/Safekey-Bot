import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_main_menu_keyboard():
    # Only a single button pointing directly to your Telegram link
    keyboard = [
        [InlineKeyboardButton("Join Our Telegram ", url="https://t.me/binary_killer2")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the welcome message with only the single channel redirect button."""
    welcome_text = (
        "This channel will be helpful for you to achieve your dream profit everyday "
        "with low risk and make you an absolute trader with the indicator."
    )
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=get_main_menu_keyboard())

async def main_async():
    """Asynchronous orchestrator initializing the framework cleanly."""
    if not BOT_TOKEN:
        logger.error("Missing BOT_TOKEN environment variable.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    # Core command handler
    application.add_handler(CommandHandler("start", start))
    
    # Callback interaction to let the start menu refresh seamlessly if needed
    application.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))

    logger.info("Bot initialized successfully. Polling activated...")
    
    # Boot framework loops
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

def main():
    """Synchronous framework initialisation wrapping the async runtime."""
    try:
        asyncio.run(main_async())
    except Exception as e:
        logger.critical(f"Bot execution loop crashed: {e}")

if __name__ == "__main__":
    main()

