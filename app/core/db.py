from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)


async_session_local = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session_local() as async_session:
        yield async_session
