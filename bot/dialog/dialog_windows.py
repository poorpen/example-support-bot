from aiogram_dialog import Dialog, Window
from ..all_states import UserState
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo
from aiogram_dialog.widgets.input import MessageInput

user_menu = Dialog(
    Window(Const('Добро пожаловать в тех поддержку\nкомпании "Ваша компания"\n\n'
                 'Выберите интересующий вас пункт'),
           Row(SwitchTo(Const("Написать обращения"), id="write_appeal", state=UserState.write_subject_appeal),
               SwitchTo(Const("Мои обращения"), id="my_appeal", state=UserState.my_appeal)),
           SwitchTo(Const("Часто задаваемые вопросы"), id="questions", state=UserState.questions),
           state=UserState.main_menu),
    # Window(Const('Введите тему обращение!\n\n'
    #              'Длина темы должна состовлять не больше 30-ти символов.'),
    #        MessageInput(),
    #        state=UserState.write_subject_appeal),
    # Window(Const('Напишите текст самого обращения и ожидайте ответа оператора!'),
    #        MessageInput(),
    #        state=UserState.write_appeal)
)
