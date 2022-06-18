from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Appeal(CallbackData, prefix="start_dialog"):
    user_id: int = None
    choice: str = None


def join_in_dialog(user_id):
    markup = InlineKeyboardBuilder()
    markup.add(
        InlineKeyboardButton(
            text="Перейти в диалог ↘️",
            callback_data=Appeal(user_id=user_id, choice="join").pack()
        )
    )
    markup.adjust(1, repeat=True)
    return markup.as_markup(resize_keyboard=True)
