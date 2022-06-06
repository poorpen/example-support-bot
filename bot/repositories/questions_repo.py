from sqlalchemy import insert, select

from bot.repositories.base_repo import BaseSQLAlchemyRepo
from bot.database.models import FrequentlyQuestions


class FrequentlyQuestionsRepo(BaseSQLAlchemyRepo):
    model = FrequentlyQuestions

    async def add_question_and_answer(self, question, answer, photo_path):
        sql = insert(self.model).values(question=question, answer=answer, photo_path=photo_path)
        await self._session.execute(sql)
        await self._session.commit()

    async def get_all_question_and_answer(self):
        sql = select(self.model)
        request = await self._session.execute(sql)
        all_question = request.scalars().all()
        return all_question
