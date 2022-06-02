from sqlalchemy import insert, select, delete, update
from bot.repositories.base_repo import BaseSQLAlchemyRepo
from bot.database.models import TelegramUser


class UserRepo(BaseSQLAlchemyRepo):
    model = TelegramUser

    async def add_user(self, telegram_id: int, first_name: str, last_name: str, username: str):
        sql = insert(self.model).values(telegram_id=telegram_id, username=username, first_name=first_name,
                                        last_name=last_name).returning('*')
        result = await self._session.execute(sql)
        await self._session.commit()
        return result.first()

    async def get_user(self, telegram_id: int):
        sql = select(self.model).where(self.model.telegram_id == telegram_id)
        request = await self._session.execute(sql)
        user = request.scalar()
        return user

    async def delete_user(self, telegram_id: int):
        sql = delete(self.model).where(self.model.telegram_id == telegram_id)
        await self._session.execute(sql)
        await self._session.commit()
