from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from typing import Sequence

from database import Category


class CategoryService:
    def __init__(self, session: sessionmaker) -> None:
        self.session: sessionmaker = session

    async def get_category_id(self, id: int) -> Category:
        async with self.session as session:
            session: AsyncSession
            category = await session.get(Category, id)
            return category

    async def get_category_name(self, name: str) -> Category or None:
        async with self.session as session:
            session: AsyncSession
            q = select(Category).where(Category.name.contains(name))
            category = await session.execute(q)
            category = category.first()
            if category:
                return category[0]
            return None
        
    async def get_all_category(self) -> Sequence[Category]:
        async with self.session as session:
            session: AsyncSession
            q = select(Category.name)
            categories = await session.execute(q)
            return categories.all()
        
    async def create_category(self, name: str) -> Category:
        async with self.session as session:
            session: AsyncSession
            category = Category(name=name)
            session.add(category)
            await session.commit()
            return category
