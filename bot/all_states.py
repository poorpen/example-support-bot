from aiogram.dispatcher.fsm.state import StatesGroup, State


class RoleState(StatesGroup):
    switch_role = State()


class UserDialogState(StatesGroup):
    waiting_the_operator = State()
    dialog = State()
    evaluate_the_operator = State()
    finish_evaluate = State()


class OperatorState(StatesGroup):
    add_photo = State()
    add_question = State()
    add_answer = State()
    show_qa = State()
    add_qa = State()
    write_name = State()
    profile = State()
    see_grades = State()


class OperatorDialogState(StatesGroup):
    get_appeal = State()
    dialog = State()
    finish_dialog = State()


class UserState(StatesGroup):
    main_menu = State()
    questions = State()
    write_appeal = State()
