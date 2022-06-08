import operator

from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Jinja
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Back, Select, Radio, Column
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import StaticMedia

from bot.all_states import UserState, UserDialogState, RoleState, OperatorState, OperatorDialogState
from bot.handlers.getters import get_operator_info, get_appeal_info, get_mark_data, get_frequently_questions, \
    get_answer_and_question, get_connected_operator, get_user_name, get_answer_data, get_answered_appeals
from bot.handlers.appeal import get_appeal_and_send, dialog
from bot.handlers.select_getter import get_role
from bot.handlers.dialog_routers import return_to_main_menu, return_to_add_question, return_to_profile
from bot.handlers.operator import get_operator_name, start_dialog, write_evaluate_operator, cancel_support
from bot.handlers.when_handlers import evaluation_check, evaluation_not_check
from bot.handlers.questions import get_question, get_answer, get_photo, add_question_and_answer, answer

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
    Window(
        Format("Добро пожаловать в профиль {name}\n"
               "Ваш рейтинг: {grade}/3 ⭐️"),
        Row(
            SwitchTo(Const("История оценок"), id='see_grades', state=OperatorState.see_grades),
            SwitchTo(Const("Изменить имя"), id='change_name', state=OperatorState.write_name), ),
        SwitchTo(Const("Добавить Вопрос/Ответ"), id='add_que', state=OperatorState.add_question),
        state=OperatorState.profile,
        getter=get_operator_info),
    Window(Jinja("Часто задаваемые вопросы:\n\n"
                 "{% for answered_appeal in answered_appeals %}"
                 "\nПользователь {{answered_appeal.user_name}}\nпоставил: {{answered_appeal.grade}} ⭐️\n\n"
                 "{% endfor %}",
                 when=lambda d, w, m: d['answered_appeals']),
           Const("Никто ещё не оценил вашу работу",
                 when=lambda d, w, m: not d['answered_appeals']),
           Back(Const("Назад")),
           state=OperatorState.see_grades,
           getter=get_answered_appeals),

    # Window(Const("Выберите категорию для вопроса"))
    Window(Const("Напишите вопрос"),
           MessageInput(get_question),
           SwitchTo(Const("Назад"), id="return", state=OperatorState.profile),
           state=OperatorState.add_question),
    Window(Const("Напиши ответ на него"),
           MessageInput(get_answer),
           Back(Const("Назад")),
           state=OperatorState.add_answer, ),
    Window(Const("Отправьте фото"),
           MessageInput(get_photo, content_types=ContentType.PHOTO),
           SwitchTo(Const("Пропустить шаг"), id="skip", state=OperatorState.show_qa),
           Back(Const("Назад")),
           state=OperatorState.add_photo,
           ),
    Window(
        StaticMedia(getter_key="photo_path", type=ContentType.PHOTO,
                    when=lambda data, w, m: data["photo_path"]),
        Format("Хотите ли вы добавить следующее:\n\n"
               "Вопрос:\n{question}\n\n"
               "Ответ:\n{answer}"),
        Row(Button(Const("Нет"), id="Ben_say_NO", on_click=return_to_profile),
            Button(Const("Да"), id="Ben_say_YES", on_click=add_question_and_answer)),
        state=OperatorState.show_qa,
        getter=get_answer_and_question

    ),
    Window(
        Const("Вы успешно добавили вопрос/ответ"),
        Button(Const("Вернуться обратно в профиль"), id='return_to_profile', on_click=return_to_profile),
        state=OperatorState.add_qa

    )
)

operator_dialog = Dialog(
    Window(Format("Поступило новое обращение!"
                  "\n\n"
                  "Имя пользователя: {name}\n\n"
                  "Текст обращения:\n"
                  "────────────────────────\n"
                  "{text}"
                  "\n\n────────────────────────\n"),
           Button(Const("Перейти в диалог ↘️"), id='start_dialog', on_click=start_dialog),
           state=OperatorDialogState.get_appeal,
           getter=get_appeal_info
           ),
    Window(
        Format("Вы на связи с пользователем {user_name}"),
        MessageInput(dialog),
        Button(Const("Завершить сеанс"), id="cancle_support", on_click=cancel_support),
        state=OperatorDialogState.dialog,
        getter=get_user_name

    ),
    Window(Format("Вы завершили чат"),
           Button(Const("Перейти в профиль"), id="return_to_profile", on_click=return_to_profile),
           state=OperatorDialogState.finish_dialog)
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
        Const("Выберите интересующий вас вопрос"),
        Const("Вопросов нет",
              when=lambda d, w, m: not d['questions']),
        Column(
            Select(
                Format("{item[0]}"),
                id='questions_',
                item_id_getter=operator.itemgetter(1),
                items="questions",
                on_click=answer
            )),
        Row(
            SwitchTo(Const("Написать обращения"), id="write_appeal", state=UserState.write_appeal),
            SwitchTo(Const("В главное меню"), id="return_manu", state=UserState.main_menu)),
        state=UserState.questions,
        getter=get_frequently_questions

    ),
    Window(
        StaticMedia(getter_key="photo_path", type=ContentType.PHOTO,
                    when=lambda data, w, m: data["photo_path"]),
        Format("{answer}"),
        Back(Const("Назад"), id="back"),
        state=UserState.andswer,
        getter=get_answer_data
    )
)

user_dialog = Dialog(
    Window(
        Const("Ваше обращение зарегистрировано. Ожидайте ответа нашего оператора в ближайшее время."),
        state=UserDialogState.waiting_the_operator),
    Window(
        Format("С вами на связи оператор {operatoname}"),
        MessageInput(dialog),
        state=UserDialogState.dialog,
        getter=get_connected_operator

    ),
    Window(
        Const("Оцените работу оператора"),
        Radio(
            Format("✓ {item[0]}"),
            Format("{item[0]}"),
            id="evaluate_operator",
            item_id_getter=operator.itemgetter(1),
            items="mark",

        ),
        Button(Const("В меню"), id="return_menu", on_click=return_to_main_menu,
               when=evaluation_not_check),
        Button(Const("Поставить оценку"), id="set_mark", on_click=write_evaluate_operator,
               when=evaluation_check),
        state=UserDialogState.evaluate_the_operator,
        getter=get_mark_data

    ),
    Window(
        Const("Спасибо за оценку!"),
        Button(Const("В меню"), id="return_menu", on_click=return_to_main_menu),
        state=UserDialogState.finish_evaluate
    )
)
