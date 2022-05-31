import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from configreader import Config, load_config
from aioredis import Redis
from database.database_utility import make_connection_string
from sqlalchemy.orm import sessionmaker
from aiogram_dialog import DialogRegistry

from bot.handlers import setup_routers
from bot.dialog import registry_dialog
from bot.middlewares import setup_middleware
from bot.database.base import metadata

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
    registry = DialogRegistry(dp)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    await setup_middleware(async_sessionmaker, dp)
    await registry_dialog(registry)
    await setup_routers(dp)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
