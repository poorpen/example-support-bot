from aiogram import Dispatcher, F
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.state import any_state

from bot.keyboard.inline.appeals_keyboard import Appeal

from . import commands, operator


class Choice(str):
    JOIN = "join"


async def register_handlers(dp: Dispatcher):
    dp.message.register(commands.switch_role, Command(commands="switchrole"), any_state)
    dp.message.register(commands.start_command, Command(commands="start"), any_state)
    dp.callback_query.register(operator.start_dialog, Appeal.filter(F.choice == Choice.JOIN))
