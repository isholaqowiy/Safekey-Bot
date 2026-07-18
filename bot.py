import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from dotenv import load_dotenv
from password_generator import generate_secure_password, evaluate_strength

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation States for Custom Password
CHOOSING_LENGTH = 1

def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📈 Join Channel", url="https://t.me/binary_killer2")],
        [InlineKeyboardButton("🔐 Generate Password", callback_data="gen_default")],
        [InlineKeyboardButton("⚙️ Custom Password", callback_data="gen_custom_init")],
        [
            InlineKeyboardButton("📋 Password Tips", callback_data="view_tips"),
            InlineKeyboardButton("❓ Help", callback_data="view_help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends the promotional welcome message with interactive menu."""
    welcome_text = (
        "This channel will be helpful for you to achieve your dream profit everyday "
        "with low risk and make you an absolute trader with the indicator."
    )
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=get_main_menu_keyboard())
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Explains bot features via /help."""
    help_text = (
        "❓ **SafeKey Bot Help Menu**\n\n"
        "• **/start** - Return to the main menu.\n"
        "• **/help** - Display this assistance manual.\n"
        "• **/tips** - Get critical advice for managing passwords.\n\n"
        "🤖 **Features:**\n"
        "1. **Generate Password**: Instant secure 16-character string.\n"
        "2. **Custom Password**: Pick specific length boundaries (8-64) and select active parameters."
    )
    if update.message:
        await update.message.reply_text(help_text, parse_mode="Markdown")
    elif update.callback_query:
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]]
        await update.callback_query.edit_message_text(help_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provides password security best practices via /tips."""
    tips_text = (
        "📋 **Password Security Best Practices**\n\n"
        "1. 🛑 **Never reuse passwords** across multiple services.\n"
        "2. 📏 Make them long—**14+ characters** is highly recommended.\n"
        "3. 🔀 Mix uppercase letters, lowercase letters, symbols, and numbers.\n"
        "4. 🧠 Avoid using names, dictionary words, birthdates, or sequential letters.\n"
        "5. 🔑 Use a trusted, reputable **Password Manager** to track everything securely."
    )
    if update.message:
        await update.message.reply_text(tips_text, parse_mode="Markdown")
    elif update.callback_query:
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]]
        await update.callback_query.edit_message_text(tips_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_default_generation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles standard fast-generation requests."""
    query = update.callback_query
    await query.answer()
    
    password = generate_secure_password()
    strength = evaluate_strength(password)
    
    response = (
        f"🔐 **Your Secure Password:**\n"
        f"`{password}`\n\n"
        f"Strength: {strength}\n"
        f"Length: 16 characters"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 Generate Another", callback_data="gen_default")],
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="main_menu")]
    ]
    await query.edit_message_text(response, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def init_custom_generation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts custom setup flow by asking for password length."""
    query = update.callback_query
    await query.answer()
    
    # Initialize defaults in context user data
    context.user_data["c_len"] = 16
    context.user_data["c_upper"] = True
    context.user_data["c_lower"] = True
    context.user_data["c_num"] = True
    context.user_data["c_sym"] = True
    
    await query.edit_message_text(
        "⚙️ **Custom Password Mode**\n\n"
        "Please type a desired password length between **8 and 64** characters:",
        parse_mode="Markdown"
    )
    return CHOOSING_LENGTH

async def process_custom_length(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validates user input length and displays structural config settings."""
    text = update.message.text
    try:
        length = int(text)
        if not (8 <= length <= 64):
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Please send a single whole number between **8 and 64**:")
        return CHOOSING_LENGTH

    context.user_data["c_len"] = length
    await show_custom_config_menu(update, context)
    return ConversationHandler.END

async def show_custom_config_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Renders toggles for customized parameters."""
    ud = context.user_data
    
    def format_toggle(label, val):
        return f"{label}: {'✅ Yes' if val else '❌ No'}"

    keyboard = [
        [InlineKeyboardButton(format_toggle("Uppercase [A-Z]", ud["c_upper"]), callback_data="toggle_upper")],
        [InlineKeyboardButton(format_toggle("Lowercase [a-z]", ud["c_lower"]), callback_data="toggle_lower")],
        [InlineKeyboardButton(format_toggle("Numbers [0-9]", ud["c_num"]), callback_data="toggle_num")],
        [InlineKeyboardButton(format_toggle("Symbols [@,#,$]", ud["c_sym"]), callback_data="toggle_sym")],
        [InlineKeyboardButton("⚡ Generate Custom Password", callback_data="gen_custom_exec")],
        [InlineKeyboardButton("⬅️ Cancel", callback_data="main_menu")]
    ]
    
    text = f"⚙️ **Configuration Matrix**\n\nLength Chosen: `{ud['c_len']}`\nSelect features to alter parameters:"
    
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_toggles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Flips configurations when structural rules buttons are interacted with."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data == "toggle_upper": context.user_data["c_upper"] = not context.user_data["c_upper"]
    elif data == "toggle_lower": context.user_data["c_lower"] = not context.user_data["c_lower"]
    elif data == "toggle_num": context.user_data["c_num"] = not context.user_data["c_num"]
    elif data == "toggle_sym": context.user_data["c_sym"] = not context.user_data["c_sym"]
    
    await show_custom_config_menu(update, context)

async def execute_custom_generation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Builds structured credentials matching rules generated during configuration."""
    query = update.callback_query
    await query.answer()
    
    ud = context.user_data
    password = generate_secure_password(
        length=ud.get("c_len", 16),
        uppercase=ud.get("c_upper", True),
        lowercase=ud.get("c_lower", True),
        numbers=ud.get("c_num", True),
        symbols=ud.get("c_sym", True)
    )
    strength = evaluate_strength(password)
    
    response = (
        f"⚡ **Custom Secure Password:**\n"
        f"`{password}`\n\n"
        f"Strength: {strength}\n"
        f"Length: {ud.get('c_len')} characters"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔄 Generate Another (Same Config)", callback_data="gen_custom_exec")],
        [InlineKeyboardButton("⚙️ Change Settings", callback_data="gen_custom_init")],
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="main_menu")]
    ]
    await query.edit_message_text(response, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def main_async():
    """Asynchronous orchestrator initializing the framework cleanly under Python 3.14+."""
    if not BOT_TOKEN:
        logger.error("Missing BOT_TOKEN environment variable.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    # Conversation logic to safely get length configurations
    custom_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(init_custom_generation, pattern="^gen_custom_init$")],
        states={
            CHOOSING_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_custom_length)]
        },
        fallbacks=[CommandHandler("start", start)],
        per_message=True
    )

    # Core commands handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tips", tips_command))
    
    # Callback interactions
    application.add_handler(custom_conv)
    application.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(help_command, pattern="^view_help$"))
    application.add_handler(CallbackQueryHandler(tips_command, pattern="^view_tips$"))
    application.add_handler(CallbackQueryHandler(handle_default_generation, pattern="^gen_default$"))
    application.add_handler(CallbackQueryHandler(handle_toggles, pattern="^toggle_"))
    application.add_handler(CallbackQueryHandler(execute_custom_generation, pattern="^gen_custom_exec$"))

    logger.info("SafeKey Bot initialized successfully. Polling activated...")
    
    # Explicitly boot framework loops for production compliance
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

