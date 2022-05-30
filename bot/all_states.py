from aiogram.dispatcher.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    main_menu = State()
