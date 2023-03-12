from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import find_dotenv, load_dotenv

from commands import register_user_commands, bot_set_commands
from database import get_session, get_engine

import logging
import asyncio
import os


async def main() -> None:
    logging.basicConfig(
        encoding='utf-8',
        level=logging.DEBUG,
        format="%(asctime)s - %(module)s - %(levelname)s - %(message)s"
    )

    load_dotenv(find_dotenv())

    storage = MemoryStorage()
    bot = Bot(token=os.getenv('token'), parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    engine = await get_engine(os.getenv('database_url'))
    session = await get_session(engine=engine)
    session = session()
    
    bot['db'] = session

    register_user_commands(dp=dp)
    await bot.set_my_commands(bot_set_commands)

    await dp.start_polling()


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemError):
        logging.warning('Bot stopped')
