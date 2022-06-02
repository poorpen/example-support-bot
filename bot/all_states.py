from aiogram.dispatcher.fsm.state import StatesGroup, State


class RoleState(StatesGroup):
    switch_role = State()


class UserDialogState(StatesGroup):
    dialog = State()
    evaluate_the_operator = State()


class OperatorState(StatesGroup):
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
    waiting_the_operator = State
