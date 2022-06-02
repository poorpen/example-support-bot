from . import commands
from aiogram import Dispatcher


async def setup_routers(dp: Dispatcher):
    dp.include_router(default_commands.router)
