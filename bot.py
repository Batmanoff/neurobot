import logging
import nest_asyncio
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

OPENROUTER_API_KEY = "token openrouter" #тут токен с опен роутера 
BOT_TOKEN = "xxxx" # тут токен с тг
MODEL = "openai/gpt-4o" #модель нейронки


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def ask_ai(message):
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": message}],
            max_tokens=100  
        )
        logging.info("API Response: %s", completion)
        if completion and completion.choices and len(completion.choices) > 0:
            return completion.choices[0].message.content
        else:
            logging.error("Unexpected API response structure: %s", completion)
            return "Ошибка: Неожиданный формат ответа от API."
    except Exception as e:
        logging.error("Exception occurred: %s", e)
        return "Ошибка: Произошла ошибка при запросе к API."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Добро пожаловать! Отправьте мне сообщение, и я отвечу.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = ask_ai(user_message)
    await update.message.reply_text(response, parse_mode="Markdown")

async def main() -> None:

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
