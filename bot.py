import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

WELCOME_MESSAGE = (
    "Assalomu alaykum! 👋\n"
    "Bosim Bobo restoraniga xush kelibsiz! 🍽️\n\n"
    "Quyidagi filiallardan birini tanlang:"
)

UNKNOWN_COMMAND_MESSAGE = (
    "Kechirasiz, bu buyruq tanilmadi.\n"
    "Filiallar ro'yxati uchun /help yuboring yoki boshlash uchun /start."
)

BRANCHES = [
    {
        "id": "somsa_jizzax",
        "name": "🥟 Bosim Bobo Somsa - Jizzax",
        "lat": 40.0992764,
        "lon": 67.9771123,
        "phone": "+998915236666",
        "phone": "+998915237777",
        "hours": "24/7",
    },
    {
        "id": "baliq",
        "name": "🐟 Bosim Bobo Baliq - Jizzax",
        "lat": 40.0958001,
        "lon": 67.9772222,
        "phone": "+998915236666",
        "phone": "+998915237777",
        "hours": "24/7",
    },
    {
        "id": "somsa_zomin",
        "name": "🥟 Bosim Bobo Somsa - Zomin",
        "lat": 39.787139,
        "lon": 68.391417,
        "phone": "+998915236666",
        "phone": "+998915237777",
        "hours": "09:00 - 22:00",
    },
]

BRANCH_BY_ID = {branch["id"]: branch for branch in BRANCHES}


def build_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(branch["name"], callback_data=branch["id"])]
        for branch in BRANCHES
    ]
    return InlineKeyboardMarkup(keyboard)


def branch_details_message(branch: dict) -> str:
    return (
        f"📍 {branch['name']}\n"
        "📞 Telefon: +998915237777\n"
        "📞 Telefon: +998915236666\n"
        f"🕐 Ish vaqti: {branch['hours']}\n\n"
        "📌 Yuqoridagi lokatsiyani bosib yo'l qurishingiz mumkin!"
    )


def branches_list_text() -> str:
    lines = ["🏪 Bosim Bobo filiallari:\n"]
    for index, branch in enumerate(BRANCHES, start=1):
        lines.append(
            f"{index}. {branch['name']}\n"
            f"   📞 {branch['phone']}\n"
            f"   🕐 {branch['hours']}\n"
        )
    lines.append("Filial tanlash uchun /start buyrug'ini yuboring.")
    return "\n".join(lines)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=build_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    await update.message.reply_text(branches_list_text())


async def branch_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return

    branch = BRANCH_BY_ID.get(query.data or "")
    if branch is None:
        await query.answer(text="Filial topilmadi.", show_alert=True)
        logger.warning("Unknown branch callback: %s", query.data)
        return

    await query.answer()

    chat_id = query.message.chat_id if query.message else query.from_user.id

    try:
        await context.bot.send_location(
            chat_id=chat_id,
            latitude=branch["lat"],
            longitude=branch["lon"],
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=branch_details_message(branch),
        )
    except TelegramError:
        logger.exception("Failed to send branch info for %s", branch["id"])
        await context.bot.send_message(
            chat_id=chat_id,
            text="Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
        )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    await update.message.reply_text(UNKNOWN_COMMAND_MESSAGE)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update %s caused error: %s", update, context.error, exc_info=context.error)


def main() -> None:
    if not ENV_PATH.is_file():
        raise SystemExit(
            f".env fayli topilmadi: {ENV_PATH}\n"
            ".env.example dan nusxa oling va BOT_TOKEN kiriting."
        )

    token = os.getenv("BOT_TOKEN")
    if not token or not token.strip():
        raise SystemExit(
            f".env faylida BOT_TOKEN bo'sh: {ENV_PATH}\n"
            "@BotFather tokenini yozing va faylni saqlang (Ctrl+S)."
        )
    if token.strip() == "your_bot_token_here":
        raise SystemExit(
            f".env da hali placeholder token bor: {ENV_PATH}\n"
            "Haqiqiy tokenni yozing va faylni saqlang (Ctrl+S)."
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(branch_selected))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    application.add_error_handler(error_handler)

    logger.info("Bot ishga tushdi")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
