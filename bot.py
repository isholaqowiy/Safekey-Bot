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

# Match your exact filenames on GitHub
PROOF_IMAGE_FILES = [
    "IMG-20260721-WA0031.jpg",
    "IMG-20260721-WA0033.jpg",
    "IMG-20260721-WA0034.jpg",
    "IMG-20260721-WA0035.jpg",
    "IMG-20260721-WA0036.jpg"
]

def get_channel_keyboard():
    """Returns a keyboard with only the call-to-action channel redirect link."""
    keyboard = [
        [InlineKeyboardButton("👉 Join Our Telegram Channel 🚀", url="https://t.me/binary_killer2")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends proof images one by one, followed by a persuasive text funnel to join the channel."""
    chat_id = update.effective_chat.id

    # 1. Loop through and send each image individually
    for filename in PROOF_IMAGE_FILES:
        if os.path.exists(filename):
            try:
                with open(filename, "rb") as f:
                    await context.bot.send_photo(chat_id=chat_id, photo=f)
                # Small delay to keep things clean and sequential in the chat
                await asyncio.sleep(0.5)
            except Exception as file_err:
                logger.error(f"Could not send image file {filename}: {file_err}")
        else:
            logger.warning(f"Image file not found in directory: {filename}")

    # 2. Persuasive conversion text
    convincing_text = (
        "📈 **Stop Gambling. Start Trading with Absolute Precision!**\n\n"
        "The results speak for themselves! Real traders are tripling their accounts and clearing "
        "thousands of dollars daily using our elite, low-risk indicators. This channel is specifically "
        "designed to help you secure consistent, daily profits while managing your risks perfectly.\n\n"
        "Whether you want to escape the cycle of losses or scale your trading account to the next level, "
        "we provide the direct setups, indicator alerts, and expert guidance to make you an absolute master "
        "of the market.\n\n"
        "👇 **Don't miss the next winning run. Click below to secure your access now!**"
    )

    # 3. Deliver the text message accompanied by the inline redirect button
    await context.bot.send_message(
        chat_id=chat_id, 
        text=convincing_text, 
        parse_mode="Markdown", 
        reply_markup=get_channel_keyboard()
    )

async def main_async():
    """Asynchronous orchestrator initializing the framework cleanly."""
    if not BOT_TOKEN:
        logger.error("Missing BOT_TOKEN environment variable.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    # Core redirection flow
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(start))

    logger.info("Redirect Bot initialized successfully. Polling activated...")
    
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
    """Synchronous framework initialisation wrapping modern async runtimes."""
    try:
        asyncio.run(main_async())
    except Exception as e:
        logger.critical(f"Bot execution loop crashed: {e}")

if __name__ == "__main__":
    main()

