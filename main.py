import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from handlers import dialog
from database.engine import init_db

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()


    print("Bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(dialog.router)
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())