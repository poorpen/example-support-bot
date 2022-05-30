from aiogram_dialog import Dialog, Window
from ..all_states import UserState
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row

user_menu = Dialog(
    Window(Const('Добро пожаловать в тех поддержку\nкомпании "Ваша компания"\n\n'
                 'Выберите интересующий вас пункт'),
           Row(Button(Const("Написать обращения"), id="write_appeal"),
               Button(Const("Мои обращения"), id="my_appeal")),
           Button(Const("Часто задаваемые вопросы"), id="questions"),
           state=UserState.main_menu),
)
