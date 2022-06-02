from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from bot.all_states import UserState


async def return_to_main_menu(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.start(UserState.main_menu)




