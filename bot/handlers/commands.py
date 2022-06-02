from aiogram import Router, types
from aiogram_dialog import DialogManager, StartMode

from bot.all_states import UserState
from bot.repositories.repo import SQLAlchemyRepo
from bot.repositories.operator_repo import OperatorRepo
from bot.repositories.user_repo import UserRepo
from bot.all_states import OperatorState, UserState, RoleState

router = Router()


@router.message(commands=["start"])
async def show_user_menu(message: types.Message, dialog_manager: DialogManager):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    user_repo: UserRepo = repo.get_repo(UserRepo)
    operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
    operator = await operator_repo.get_operator(message.from_user.id)
    user = await user_repo.get_user(message.from_user.id)
    if operator:
        state = OperatorState.profile
    elif user:
        state = UserState.main_menu
    else:
        state = RoleState.switch_role
    await dialog_manager.start(state, mode=StartMode.RESET_STACK)


@router.message(commands=["switchrole"])
async def switch_role(message: types.Message, dialog_manager: DialogManager):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    user_repo: UserRepo = repo.get_repo(UserRepo)
    operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
    await user_repo.delete_user(telegram_id=message.from_user.id)
    await operator_repo.delete_operator(telegram_id=message.from_user.id)
    await dialog_manager.start(RoleState.switch_role)
