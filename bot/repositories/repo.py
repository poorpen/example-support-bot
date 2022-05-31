from .base_repo import BaseSQLAlchemyRepo
from typing import Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from functools import lru_cache

BaseSQLAlchemyRepoType = TypeVar("BaseSQLAlchemyRepoType", bound=BaseSQLAlchemyRepo)


class SQLAlchemyRepo:

    def __init__(self, session: AsyncSession):
        self._session = session

    @lru_cache()
    def get_repo(self, repo: Type[BaseSQLAlchemyRepo]) -> BaseSQLAlchemyRepoType:
        return repo(self._session)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
