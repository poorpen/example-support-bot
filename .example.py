import asyncio

from typing import Any
from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram import types
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram_dialog import StartMode, DialogManager, DialogRegistry, Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

TOKEN = "5517542216:AAG4xmVe2SZnP7h4bAye56_8wfmKlT1W954"


class UserState(StatesGroup):
    main_menu = State()
    change_state = State()
    i_changed_state = State()
    changed_state = State()


router = Router()


@router.message(commands=["start"])
async def show_user_menu(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserState.change_state, mode=StartMode.RESET_STACK)


async def change_state(call: types.CallbackQuery, widget: Any, dialog_manager: DialogManager):
    pupa_manager = dialog_manager.bg(user_id=455559956, chat_id=455559956)
    await pupa_manager.start(UserState.changed_state, mode=StartMode.RESET_STACK)
    await dialog_manager.switch_to(UserState.i_changed_state)


async def registry_dialog(registry: DialogRegistry):
    registry.register(user_menu)


async def setup_routers(dp: Dispatcher):
    dp.include_router(router)


user_menu = Dialog(
    Window(Const("Изменить состояние пользователя Пупа"),
           Button(Const("Изменить состояние"), id='change_state', on_click=change_state),
           state=UserState.change_state),
    Window(Const("Попытка изменить состояние"),
           state=UserState.i_changed_state),
    Window(Const("Изменили состояние"),
           state=UserState.changed_state)
)


async def main():
    # redis_connect = Redis.from_url(config.redis.host, password=config.redis.password)
    # storage = RedisStorage(redis_connect, key_builder=DefaultKeyBuilder(with_destiny=True))
    storage = MemoryStorage()
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    registry = DialogRegistry(dp)
    await registry_dialog(registry)
    await setup_routers(dp)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
