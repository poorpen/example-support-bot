import os

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram_dialog import DialogManager, Dialog, ShowMode, StartMode
from typing import Any

from bot.repositories.repo import SQLAlchemyRepo
from bot.repositories.questions_repo import FrequentlyQuestionsRepo
from bot.all_states import OperatorState


# repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
# question: FrequentlyQuestionsRepo = repo.get_repo(FrequentlyQuestionsRepo)

async def get_question(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    dialog_manager.current_context().dialog_data.update(question=message.text)
    await dialog_manager.switch_to(OperatorState.add_answer)


async def get_answer(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    dialog_manager.current_context().dialog_data.update(answer=message.text)
    await dialog_manager.switch_to(OperatorState.add_photo)


async def get_photo(message: Message, dialog: Dialog, dialog_manager: DialogManager):
    bot: Bot = dialog_manager.data.get('bot')
    photo_size: PhotoSize = message.photo[-1]
    file_info = await bot.get_file(file_id=photo_size.file_id)
    bot_path = os.path.abspath(".")
    full_path = f"{bot_path}/{file_info.file_path}"
    await bot.download_file(file_info.file_path, full_path)
    dialog_manager.current_context().dialog_data.update(photo_path=full_path)
    await dialog_manager.switch_to(OperatorState.show_qa)
    # src = f'bot/photos/{file_info.file_id}.jpeg'
    # with open(src, 'wb') as new_file:
    #     new_file.write(downloaded_file)
    # # file_info =
    # file_info =


async def add_question_and_answer(call: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    repo: SQLAlchemyRepo = dialog_manager.data.get('repo')
    frequently_questions_repo: FrequentlyQuestionsRepo = repo.get_repo(FrequentlyQuestionsRepo)
    photo_path = dialog_manager.current_context().dialog_data.get('photo_path')
    question = dialog_manager.current_context().dialog_data.get("question")
    answer = dialog_manager.current_context().dialog_data.get("answer")
    await frequently_questions_repo.add_question_and_answer(question=question, answer=answer, photo_path=photo_path)
    await dialog_manager.switch_to(OperatorState.add_qa)
