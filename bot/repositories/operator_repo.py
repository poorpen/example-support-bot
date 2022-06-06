from sqlalchemy import insert, select, update, delete

from bot.repositories.base_repo import BaseSQLAlchemyRepo
from bot.database.models import Operator


class OperatorRepo(BaseSQLAlchemyRepo):
    model = Operator

    async def get_operator(self, telegram_id):
        sql = select(self.model).where(self.model.telegram_id == telegram_id)
        request = await self._session.execute(sql)
        operator = request.scalar()
        return operator

    async def get_all_operators_id(self):
        sql = select(self.model.telegram_id)
        request = await self._session.execute(sql)
        all_id = request.scalars().all()
        return all_id

    async def update_name(self, telegram_id, name):
        sql = update(self.model).where(self.model.telegram_id == telegram_id).values(name=name)
        await self._session.execute(sql)
        await self._session.commit()

    async def delete_operator(self, telegram_id):
        sql = delete(self.model).where(self.model.telegram_id == telegram_id)
        await self._session.execute(sql)
        await self._session.commit()

    async def add_operator(self, telegram_id, name=None):
        sql = insert(self.model).values(telegram_id=telegram_id, name=name).returning('*')
        request = await self._session.execute(sql)
        await self._session.commit()
        return request.first()
