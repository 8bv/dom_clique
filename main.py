import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dom_clique.config import load_config
from dom_clique.handlers import register_user

logger = logging.getLogger(__name__)


async def setup():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("config.ini")

    bot = Bot(token=config.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_user(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def main():
    try:
        asyncio.run(setup())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    main()
