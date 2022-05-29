import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from configreader import Config, load_config
from aioredis import Redis
from database.database_utility import make_connection_string
from sqlalchemy.orm import sessionmaker


async def main():
    config: Config = load_config()
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    engine = create_async_engine(make_connection_string(config.db), future=True)
    async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    redis_connect = Redis.from_url(config.redis.host, password=config.redis.password)
    storage = RedisStorage(redis_connect, key_builder=DefaultKeyBuilder(with_destiny=True))
    bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), redis=redis_connect)
