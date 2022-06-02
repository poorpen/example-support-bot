from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, Dialog
from aioredis import Redis
from typing import Any

from bot.all_states import OperatorState, UserDialogState, UserState, OperatorDialogState
from bot.repositories.repo import SQLAlchemyRepo
from bot.repositories.operator_repo import OperatorRepo
from bot.all_states import OperatorState
from bot.database.models import Operator


async def get_operator_name(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
    telegram_user = dialog_manager.data.get('event_chat')
    operator = await operator_repo.get_operator(telegram_user.id)
    if operator is None:
        operator: Operator = await operator_repo.add_operator(telegram_id=telegram_user.id, name=message.text)
    else:
        await operator_repo.update_name(telegram_id=telegram_user.id, name=message.text)
    dialog_manager.current_context().dialog_data.update(name=operator.name, rating=operator.average_rating)
    await dialog_manager.switch_to(OperatorState.profile)


async def start_dialog(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    bot: Bot = dialog_manager.data.get('bot')
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
    operator: Operator = await operator_repo.get_operator(call.from_user.id)
    redis_conn: Redis = dialog_manager.data.get('redis_conn')

    companion_id = dialog_manager.current_context().start_data.get('companion_id')
    companion_state = redis_conn.hget(f'{companion_id}_data', "state")
    if companion_state == UserState.waiting_the_operator.__str__():
        companion_manager = dialog_manager.bg(user_id=companion_id, chat_id=companion_id)
        await companion_manager.start(state=UserDialogState.dialog, data={'companion_id': call.from_user.id})
        await bot.send_message(chat_id=companion_id, text=f"С вами на связи оператор {operator.name}")
        await dialog_manager.start(OperatorDialogState.dialog, data={'companion_id': companion_id})
