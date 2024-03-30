from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Text, BigInteger, ForeignKey, Date, Time


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Direction(Base):
    __tablename__ = 'direction'
    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text)

    sessions: Mapped[list['Session']] = relationship("Session", back_populates="direction")

    def __repr__(self):
        return f'id: {self.id} title: {self.title}'


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    phone_number: Mapped[str]
    tg_id: Mapped[int] = mapped_column(BigInteger)

    session_records: Mapped[list['SessionRecord']] = relationship("SessionRecord", back_populates="user")


class Session(Base):
    __tablename__ = 'session'
    direction_id: Mapped[int] = mapped_column(ForeignKey('direction.id'))
    direction: Mapped[Direction] = relationship(back_populates="sessions")

    data: Mapped[Date] = mapped_column(Date)
    time: Mapped[Time] = mapped_column(Time)

    session_records: Mapped[list['SessionRecord']] = relationship("SessionRecord", back_populates="session")


class SessionRecord(Base):
    __tablename__ = 'session_record'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(back_populates="session_records")

    session_id: Mapped[int] = mapped_column(ForeignKey('session.id'))
    session: Mapped[Session] = relationship(back_populates="session_records")
