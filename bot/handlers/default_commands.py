from aiogram import Router, types
from aiogram_dialog import DialogManager, StartMode
from ..all_states import UserState

router = Router()


@router.message(commands=["start"])
async def show_user_menu(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserState.main_menu, mode=StartMode.RESET_STACK)
