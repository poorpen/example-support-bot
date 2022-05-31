from aiogram.dispatcher.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    main_menu = State()
    write_subject_appeal = State()
    write_appeal = State()
    questions = State()
    my_appeal = State()

