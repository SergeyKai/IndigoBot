from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Text, BigInteger, ForeignKey, Date, Time


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Direction(Base):
    __tablename__ = 'directions'
    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text)

    sessions: Mapped[list['Sessions']] = relationship("Sessions", back_populates="direction")

    def __repr__(self):
        return f'id: {self.id} title: {self.title}'


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str]
    phone_number: Mapped[str]
    tg_id: Mapped[int] = mapped_column(BigInteger)

    sessions_record: Mapped[list['SessionRecord']] = relationship("SessionRecord", back_populates="user")


class Sessions(Base):
    __tablename__ = 'sessions'
    direction: Mapped[Direction] = relationship(Direction, back_populates="sessions")
    direction_id: Mapped[int] = relationship(ForeignKey('direction'))

    data: Mapped[Date] = mapped_column(Date)
    time: Mapped[Time] = mapped_column(Time)

    sessions_record: Mapped[list['SessionRecord']] = relationship("SessionRecord", back_populates="session")


class SessionRecord(Base):
    __tablename__ = 'session_record'
    user: Mapped[User] = relationship(User, back_populates="session_records")
    user_id: Mapped[int] = relationship(ForeignKey('users'))

    session: Mapped[Sessions] = relationship(Sessions, back_populates="session_records")
    session_id: Mapped[int] = relationship(ForeignKey('sessions'))
