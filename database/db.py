from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from .tables import Base


async def get_engine(url: str, create_new: bool = False) -> AsyncEngine:
    engine = create_async_engine(url, echo=True)
    if create_new:
        await init_models(engine=engine)
    return engine


async def get_session(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_models(engine: AsyncEngine) -> None:
    async with engine.begin() as db:
        await db.run_sync(Base.metadata.drop_all)
        await db.run_sync(Base.metadata.create_all)
