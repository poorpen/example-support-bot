from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message
from typing import Any, Awaitable, Callable, Dict
from aioredis.client import Redis
from aiogram_dialog import DialogManager


class WriteUserState(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message or CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        await handler(event, data)
        telegram_user = data.get('event_chat')
        conn: Redis = data.get('redis_conn')
        dialog_manager: DialogManager = data.get('dialog_manager')
        current_context = dialog_manager.current_context()
        if current_context:
            state = current_context.state
            await conn.hset(f"{telegram_user.id}_data", key="state", value=state.__str__())
