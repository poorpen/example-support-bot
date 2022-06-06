from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.state import any_state
from . import commands


async def register_handlers(dp: Dispatcher):
    dp.message.register(commands.switch_role, Command(commands="switchrole"), any_state)
    dp.message.register(commands.start_command, Command(commands="start"), any_state)


async def setup_routers(dp: Dispatcher):
    dp.include_router(commands.router)
