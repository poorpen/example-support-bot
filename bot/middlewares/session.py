from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import TelegramObject
from sqlalchemy.orm import sessionmaker


class GetConnectionToDB(BaseMiddleware):

    def __init__(self, sm: sessionmaker):
        self._session = sm

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with self._session() as session:
            data['session'] = session
            await handler(event, data)
            data.pop('session')
