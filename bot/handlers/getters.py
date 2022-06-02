from aiogram_dialog import DialogManager

from bot.repositories.repo import SQLAlchemyRepo
from bot.repositories.operator_repo import OperatorRepo
from bot.database.models import Operator


async def get_operator_info(dialog_manager: DialogManager, **kwargs):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    dialog_data = dialog_manager.current_context().dialog_data
    if dialog_data:
        name = dialog_data.get('name')
        rating = dialog_data.get('rating')
    else:
        telegram_user = dialog_manager.data.get('event_chat')
        operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
        operator: Operator = await operator_repo.get_operator(telegram_id=telegram_user.id)
        name = operator.name
        rating = operator.average_rating
    return {
        'grade': rating,
        'name': name
    }


async def get_appeal_info(dialog_manager: DialogManager, **kwargs):
    name = dialog_manager.current_context().start_data.get('name')
    text = dialog_manager.current_context().start_data.get('appeal')
    return {
        "name": name,
        "text": text
    }