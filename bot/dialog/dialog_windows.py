import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Back, Select
from aiogram_dialog.widgets.input import MessageInput, TextInput

from bot.all_states import UserState, UserDialogState, RoleState, OperatorState, OperatorDialogState
from bot.handlers.getters import get_operator_info, get_appeal_info
from bot.handlers.appeal import get_appeal_and_send
from bot.handlers.select_getter import get_role
from bot.handlers.dialog_routers import return_to_main_menu
from bot.handlers.operator import get_operator_name, start_dialog

role_reversal = Dialog(
    Window(
        Const('За кого бы вы хотели протестировать бота'),
        Select(
            Format("{item[0]}"),
            id='switch_role',
            item_id_getter=operator.itemgetter(1),
            items=[('За оператора', "oper"), ("За пользователя", 'user')],
            on_click=get_role,
        ),
        state=RoleState.switch_role
    )
)

operator_menu = Dialog(
    Window(Format("Укажите ваше имя"),
           MessageInput(get_operator_name),
           state=OperatorState.write_name),
    Window(Format("Добро пожаловать в профиль {name}\n"
                  "Ваш рейтинг: {grade}/3 ⭐️"),
           SwitchTo(Const("Оценки пользователей"), id='see_grades', state=OperatorState.see_grades),
           SwitchTo(Const("Изменить имя"), id='change_name', state=OperatorState.write_name),
           state=OperatorState.profile,
           getter=get_operator_info)
)

operator_dialog = Dialog(
    Window(Const("Поступило новое обращение от {name}"
                 "\n\n"
                 "Текст обращения:"
                 "{text}"),
           SwitchTo(Const("Перейти в диалог ↘️"), state=OperatorDialogState.dialog, id='start_dialog',
                    on_click=start_dialog),
           state=OperatorDialogState.get_appeal,
           getter=get_operator_info
           ),
)

user_menu = Dialog(
    Window(Const('Добро пожаловать в тех поддержку\nкомпании "Ваша компания"\n\n'
                 'Выберите интересующий вас пункт'),
           SwitchTo(Const("Написать обращения"), id="write_appeal", state=UserState.write_appeal),
           SwitchTo(Const("Часто задаваемые вопросы"), id="questions", state=UserState.questions),
           state=UserState.main_menu),
    Window(Const('Напишите ваше обращения'),
           Back(),
           MessageInput(get_appeal_and_send),
           state=UserState.write_appeal),
    Window(
        Const("Ваше обращение зарегистрировано. Ожидайте ответа нашего оператора в ближайшее время."),
        state=UserState.waiting_the_operator),
)

user_dialog = Dialog(
    Window(
        MessageInput(),
        state=UserDialogState.dialog

    )
)