from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from bot.database.base import Base


class Operator(Base):
    __tablename__ = "operator"
    telegram_id = Column(BigInteger, nullable=False, default=None, primary_key=True)
    name = Column(String(length=20))
    average_rating = Column(Integer, default=0)
    answered_appeals = relationship("AnsweredAppeals", lazy="joined", cascade="all, delete-orphan")


class TelegramUser(Base):
    __tablename__ = "telegram_user"
    telegram_id = Column(BigInteger, nullable=False, default=None, primary_key=True)
    username = Column(String(length=100), nullable=True)
    first_name = Column(String(length=60), nullable=False)
    last_name = Column(String(length=60), nullable=True)


class AnsweredAppeals(Base):
    __tablename__ = 'answered_appeals'
    id = Column(Integer, primary_key=True)
    operator_id = Column(BigInteger, ForeignKey('operator.telegram_id'))
    user_name = Column(String, ForeignKey('telegram_user.first_name'))
    grade = Column(Integer)
