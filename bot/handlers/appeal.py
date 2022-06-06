from aiogram.types import Message
from aiogram_dialog import DialogManager, Dialog, ShowMode, StartMode
from aioredis import Redis

from bot.all_states import UserDialogState, OperatorDialogState, UserState, OperatorState
from bot.repositories.repo import SQLAlchemyRepo
from bot.repositories.operator_repo import OperatorRepo


async def send_appeal(all_id, telegram_user, appeal: str, redis_conn: Redis, dialog_manager: DialogManager):
    for oper_id in all_id:
        state = await redis_conn.hget(f"{oper_id}_data", "state")
        if state:
            state = state.decode('utf-8')
            if state != OperatorDialogState.dialog.__str__():
                operator_manager = dialog_manager.bg(chat_id=oper_id, user_id=oper_id)
                if state == OperatorState.profile.__str__():
                    mode = StartMode.RESET_STACK
                else:
                    mode = StartMode.NEW_STACK
                await operator_manager.start(OperatorDialogState.get_appeal, mode=mode,
                                             data={'companion_id': telegram_user.id,
                                                   'name': telegram_user.first_name,
                                                   'appeal': appeal})
                await redis_conn.hset(f"{oper_id}_data", key="state",
                                      value=OperatorDialogState.get_appeal.__str__())


async def get_appeal_and_send(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    redis_conn: Redis = dialog_manager.data.get('redis_conn')
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    telegram_user = dialog_manager.data.get('event_chat')
    operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
    all_id = await operator_repo.get_all_operators_id()
    appeal = message.text
    await send_appeal(all_id, telegram_user, appeal, redis_conn, dialog_manager)
    await dialog_manager.start(state=UserDialogState.waiting_the_operator, mode=StartMode.RESET_STACK)


async def dialog(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    companion_id = dialog_manager.current_context().start_data.get("companion_id")
    dialog_manager.show_mode = ShowMode.EDIT
    await message.copy_to(chat_id=companion_id)
