from aiogram.types import CallbackQuery
from typing import Any
from aiogram_dialog import DialogManager

from bot.repositories.repo import SQLAlchemyRepo
from bot.database.models import TelegramUser, Operator
from bot.repositories.user_repo import UserRepo
from bot.repositories.operator_repo import OperatorRepo
from bot.all_states import UserState, OperatorState


async def get_role(call: CallbackQuery, widget: Any, dialog_manager: DialogManager, role: str):
    telegram_user = dialog_manager.data.get('event_chat')
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    if role == 'oper':
        operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
        await operator_repo.add_operator(telegram_id=telegram_user.id)
        state = UserState.main_menu
    else:
        user_repo: UserRepo = repo.get_repo(UserRepo)
        await user_repo.add_user(telegram_id=telegram_user.id,
                                 username=telegram_user.username,
                                 first_name=telegram_user.first_name,
                                 last_name=telegram_user.last_name
                                 )
        state = OperatorState.profile
    await dialog_manager.start(state)
