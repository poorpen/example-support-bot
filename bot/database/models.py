from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from bot.database.base import Base


class Operator(Base):
    __tablename__ = "operator"
    telegram_id = Column(BigInteger, nullable=False, default=None, primary_key=True)
    password = Column(String)


class User(Base):
    __tablename__ = "telegram_user"
    telegram_id = Column(BigInteger, nullable=False, default=None, primary_key=True)
    username = Column(String(length=100), nullable=True)
    first_name = Column(String(length=60), nullable=False)
    last_name = Column(String(length=60), nullable=True)
    appeals = relationship("Appeals", lazy="joined", cascade="all, delete-orphan")


class Appeals(Base):
    __tablename__ = 'appeals'
    appeals_id = Column(Integer, primary_key=True)
    appeals_theme = Column(String(length=30))
    appeals_text = Column(Text)
    telegram_id = Column(BigInteger, ForeignKey('telegram_user.telegram_id'))
