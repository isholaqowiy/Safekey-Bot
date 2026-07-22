import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
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

# List of image URLs or file paths on your hosting server/environment
# Replace these strings with your actual image paths or Telegram file IDs
PROOF_IMAGES = [
    "path/to/image1.jpg", # 1000222515.jpg
    "path/to/image2.jpg", # 1000222518.jpg
    "path/to/image3.jpg", # 1000222521.jpg
    "path/to/image4.jpg", # 1000222524.jpg
    "path/to/image5.jpg"  # 1000222527.jpg
]

def get_channel_keyboard():
    """Returns a keyboard with only the call-to-action channel redirect link."""
    keyboard = [
        [InlineKeyboardButton("👉 Join Our Telegram Channel 🚀", url="https://t.me/binary_killer2")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends proof images first, followed by a persuasive text funnel to join the channel."""
    chat_id = update.effective_chat.id

    # 1. Send the proof images as an album first if files are configured
    media_group = []
    for img in PROOF_IMAGES:
        if os.path.exists(img) or img.startswith("http") or img.isalnum(): # supports local path, url, or file_id
            media_group.append(InputMediaPhoto(media=img))
            
    if media_group:
        try:
            await context.bot.send_media_group(chat_id=chat_id, media=media_group)
        except Exception as e:
            logger.error(f"Failed to send proof images: {e}")

    # 2. Persuasive and meaningful conversion text
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

    # 3. Deliver the message accompanied by the inline conversion button
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
