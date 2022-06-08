from bot.repositories.base_repo import BaseSQLAlchemyRepo
from bot.database.models import AnsweredAppeals, Operator


class AnsweredAppealsRepo(BaseSQLAlchemyRepo):
    model = AnsweredAppeals

    async def add_rating(self, operator: Operator, mark: int, username: str):
        rating = self.model(operator_id=operator.telegram_id, user_name=username, grade=mark)
        operator.answered_appeals.append(rating)
        average_rating = 0
        for appeal in operator.answered_appeals:
            average_rating += appeal.grade
        average_rating = average_rating / len(operator.answered_appeals)
        operator.average_rating = average_rating
        await self._session.commit()



