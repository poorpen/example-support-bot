from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.repositories.repo import SQLAlchemyRepo
from bot.repositories.user_repo import UserRepo
from bot.database.models import User


class ExistUser(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        telegram_user = data.get('event_chat')
        repo: SQLAlchemyRepo = data.get('repo')
        user_repo: UserRepo = repo.get_repo(UserRepo)
        user: User = await user_repo.get_user(telegram_user.id)
        if user is None:
            user = await repo.get_repo(UserRepo).add_user(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
            )
        data['user'] = user
        await handler(event, data)
        data.pop('user')
