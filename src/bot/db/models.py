from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, BigInteger


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Direction(Base):
    __tablename__ = 'directions'
    title: Mapped[str]
    description: Mapped[Text]


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    phone_number: Mapped[str]
    tg_id: Mapped[BigInteger]
