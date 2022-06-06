from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog

from bot.all_states import UserState, OperatorState


async def return_to_add_question(call: CallbackQuery, dialog: Dialog, dialog_manager: DialogManager):
    await dialog_manager.start(OperatorState.add_question, mode=StartMode.NORMAL)


async def return_to_main_menu(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.start(UserState.main_menu)


async def return_to_profile(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.start(OperatorState.profile)



