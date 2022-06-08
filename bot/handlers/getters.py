from aiogram_dialog import DialogManager
from ..utils import check_float_end

from bot.repositories.repo import SQLAlchemyRepo
from bot.repositories.operator_repo import OperatorRepo
from bot.repositories.questions_repo import FrequentlyQuestionsRepo
from bot.database.models import Operator


async def get_operator_info(dialog_manager: DialogManager, **kwargs):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    dialog_data = dialog_manager.current_context().dialog_data
    name = dialog_data.get('name')
    rating = dialog_data.get('rating')
    if not name or not rating:
        telegram_user = dialog_manager.data.get('event_chat')
        operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
        operator: Operator = await operator_repo.get_operator(telegram_id=telegram_user.id)
        name = operator.name
        rating = operator.average_rating
    rating = check_float_end(rating, ".0")
    return {
        'grade': rating,
        'name': name
    }


async def get_answered_appeals(dialog_manager: DialogManager, **kwargs):
    telegram_user = dialog_manager.data.get('event_chat')
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    operator_repo: OperatorRepo = repo.get_repo(OperatorRepo)
    operator: Operator = await operator_repo.get_operator(telegram_user.id)
    answered_appeals = operator.answered_appeals
    return {
        "answered_appeals": answered_appeals
    }


async def get_answer_and_question(dialog_manager: DialogManager, **kwargs):
    photo_path = dialog_manager.current_context().dialog_data.get('photo_path')
    answer = dialog_manager.current_context().dialog_data.get('answer')
    question = dialog_manager.current_context().dialog_data.get('question')
    return {
        "photo_path": photo_path,
        "question": question,
        "answer": answer
    }


async def get_frequently_questions(dialog_manager: DialogManager, **kwargs):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    frequently_questions_repo: FrequentlyQuestionsRepo = repo.get_repo(FrequentlyQuestionsRepo)
    all_question = await frequently_questions_repo.get_all_question_and_answer()
    questions = list()
    for question in all_question:
        questions.append((f"{question.id}. {question.question}", f"{question.id}"))
    return {
        "questions": questions
    }


async def get_answer_data(dialog_manager: DialogManager, **kwargs):
    answer = dialog_manager.current_context().dialog_data.get("answer")
    photo_path = dialog_manager.current_context().dialog_data.get("photo_path")
    return {
        "answer": answer,
        "photo_path": photo_path
    }


async def get_appeal_info(dialog_manager: DialogManager, **kwargs):
    name = dialog_manager.current_context().start_data.get('name')
    text = dialog_manager.current_context().start_data.get('appeal')
    return {
        "name": name,
        "text": text
    }


async def get_mark_data(dialog_manager: DialogManager, **kwargs):
    mark = [
        ("☹️", "1"),
        ("😐", "2"),
        ("😃", "3")
    ]
    return {
        "mark": mark
    }


async def get_connected_operator(dialog_manager: DialogManager, **kwargs):
    name = dialog_manager.current_context().start_data.get("name")
    return {
        "operatoname": name
    }


async def get_user_name(dialog_manager: DialogManager, **kwargs):
    name = dialog_manager.current_context().start_data.get("user_name")
    return {
        "user_name": name
    }
