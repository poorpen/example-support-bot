from aiogram import Bot
from aiogram.types import Message, CallbackQuery, Update
from aiogram_dialog import DialogManager, Dialog, StartMode
from aiogram_dialog.widgets.kbd import ManagedRadioAdapter
from aioredis import Redis
from typing import Any

from bot.all_states import OperatorState, UserDialogState, UserState, OperatorDialogState
from bot.repositories.repo import SQLAlchemyRepo
from bot.repositories.operator_repo import OperatorRepo
from bot.repositories.answered_appeals_repo import AnsweredAppealsRepo
from bot.database.models import Operator


async def get_operator_name(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
    telegram_user = dialog_manager.data.get('event_chat')
    operator: Operator = await operator_repo.get_operator(telegram_user.id)
    if operator is None:
        operator: Operator = await operator_repo.add_operator(telegram_id=telegram_user.id, name=message.text)
    else:
        await operator_repo.update_name(telegram_id=telegram_user.id, name=message.text)
    dialog_manager.current_context().dialog_data.update(name=operator.name, rating=operator.average_rating)
    await dialog_manager.switch_to(OperatorState.profile)


async def start_dialog(call: CallbackQuery, widget: Any=None, dialog_manager: DialogManager=None, **kwargs):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    bot: Bot = dialog_manager.data.get('bot')
    operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
    operator: Operator = await operator_repo.get_operator(call.from_user.id)
    redis_conn: Redis = dialog_manager.data.get('redis_conn')
    update: Update = kwargs['event_update']
    data = update.callback_query.data.split(':')
    companion_id = int(data[1])
    companion_state = await redis_conn.hget(f'{companion_id}_data', "state")
    companion_state = companion_state.decode('utf-8')
    if companion_state == UserDialogState.waiting_the_operator.__str__():
        message_id = await redis_conn.hget(f'appeal_{companion_id}_id', "message")
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=int(message_id))
        companion_manager = dialog_manager.bg(user_id=companion_id, chat_id=companion_id)
        await companion_manager.start(state=UserDialogState.dialog, mode=StartMode.RESET_STACK,
                                      data={'companion_id': call.from_user.id,
                                            "name": operator.name})
        await redis_conn.hset(f"{companion_id}_data", key="state",
                              value=UserDialogState.dialog.__str__())
        await dialog_manager.start(OperatorDialogState.dialog, mode=StartMode.RESET_STACK,
                                   data={'companion_id': companion_id})
    else:
        await call.answer(text="Пользователь общается с другим оператором", show_alert=True)


async def cancel_support(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    companion_id = dialog_manager.current_context().start_data.get('companion_id')
    companion_manager = dialog_manager.bg(user_id=companion_id, chat_id=companion_id)
    await dialog_manager.start(OperatorDialogState.finish_dialog, mode=StartMode.RESET_STACK)
    await companion_manager.start(UserDialogState.evaluate_the_operator, mode=StartMode.RESET_STACK,
                                  data={"companion_id": call.from_user.id})


async def write_evaluate_operator(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
    answered_appeals_repo: AnsweredAppealsRepo = repo.get_repo(AnsweredAppealsRepo)
    dialog_manager.dialog().find("evaluate_operator")
    mark_radio: ManagedRadioAdapter = dialog_manager.dialog().find('evaluate_operator')
    mark = mark_radio.get_checked()
    if mark:
        mark = int(mark)
        companion_id = dialog_manager.current_context().start_data.get('companion_id')
        operator = await operator_repo.get_operator(companion_id)
        await answered_appeals_repo.add_rating(operator, mark, call.from_user.first_name)
        await dialog_manager.switch_to(UserDialogState.finish_evaluate)
