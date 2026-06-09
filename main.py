import os
import random
import logging
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

QUESTIONS = [
    "Привет 🌿 Как ты сейчас себя чувствуешь?",
    "Эй, я тут 💙 Как ты сейчас?",
    "Момент для паузы ✨ Как твоё состояние прямо сейчас?",
    "Останови на секунду 🌸 Что происходит внутри?",
    "Просто хочу спросить 💚 Как ты?",
]


async def start(update: Update, context):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"Привет! Бот запущен 💚\n\nТвой chat_id: {chat_id}\n\nСохрани его — он понадобится для настройки."
    )


async def handle_message(update: Update, context):
    await update.message.reply_text("Спасибо, что ответил(а)! Я вернусь позже 🌱")


async def send_checkin(context):
    if CHAT_ID:
        question = random.choice(QUESTIONS)
        await context.bot.send_message(chat_id=int(CHAT_ID), text=question)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    job_queue = app.job_queue
    job_queue.run_daily(send_checkin, time=time(6, 0))
    job_queue.run_daily(send_checkin, time=time(11, 0))
    job_queue.run_daily(send_checkin, time=time(17, 0))

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
