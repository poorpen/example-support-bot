from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker
from aioredis.client import Redis

from bot.middlewares.repo import Repository
from bot.middlewares.session import GetConnectionToDB
from bot.middlewares.redis_connection import GetConnectionToRedis
from bot.middlewares.write_user_state import WriteUserState


async def setup_middleware(sm: sessionmaker, redis: Redis, dp: Dispatcher):
    dp.message.middleware(GetConnectionToRedis(redis))
    dp.message.middleware(GetConnectionToDB(sm))
    dp.message.middleware(Repository())
    dp.message.middleware(WriteUserState())

    dp.callback_query.middleware(GetConnectionToRedis(redis))
    dp.callback_query.middleware(GetConnectionToDB(sm))
    dp.callback_query.middleware(Repository())
    dp.callback_query.middleware(WriteUserState())
