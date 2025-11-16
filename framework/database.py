from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+aiomysql://app_user:messagingDB@34.57.117.148:3306/messaging_db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
