from bot.middlewares.exist_user import ExistUser
from bot.middlewares.repo import Repository
from bot.middlewares.session import GetConnectionToDB

from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker


async def setup_middleware(sm: sessionmaker, dp: Dispatcher):
    dp.message.middleware(GetConnectionToDB(sm))
    dp.message.middleware(Repository())
    dp.message.middleware(ExistUser())

    dp.callback_query.middleware(GetConnectionToDB(sm))
    dp.callback_query.middleware(Repository())
    dp.callback_query.middleware(ExistUser())
