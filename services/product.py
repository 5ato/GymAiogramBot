from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from aiogram.dispatcher.storage import FSMContextProxy

from typing import Sequence

from database import Product, Category


class ProductService:
    def __init__(self, session: sessionmaker) -> None:
        self.session: sessionmaker = session

    async def create_product(self, data: FSMContextProxy) -> Product:
        async with self.session as session:
            session: AsyncSession
            product = Product(
                name=data['name'], prcie=data['price'], description=data['description'], image=data['image'],
                user_id_created=data['user_id_created'], category_id=data['category_id']
            )
            session.add(product)
            await session.commit()
            return product
        
    async def get_all_products(self) -> Sequence[Product]:
        async with self.session as session:
            session: AsyncSession
            q = select(Product.name, Product.prcie, Product.description, Product.image)
            result = await session.execute(q)
            return result.all() 
