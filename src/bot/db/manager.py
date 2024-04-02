from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.settings import DBConfig


class SessionFactory:
    CONN_URL = DBConfig.DB_URL

    def __init__(self, ):
        self.engine = create_async_engine(self.CONN_URL, echo=True)
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
