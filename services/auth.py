from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update

from aiogram.dispatcher.storage import FSMContextProxy

from database import User

from typing import Sequence, Optional
import logging


class AuthService:
    def __init__(self, session: sessionmaker) -> None:
        self.session: sessionmaker = session

    async def _get_user(self, telegram_id: str) -> User:
        async with self.session as session:
            session: AsyncSession
            q = select(User).where(User.telegram_id_user == telegram_id)
            user = await session.execute(q)
            user = user.first()
            if user:
                return user[0]
            return None

    async def get_user(self, telegram_id: str) -> User:
        return await self._get_user(telegram_id=telegram_id)
    
    async def get_all_users(self) -> Sequence[User]:
        async with self.session as session:
            session: AsyncSession
            q = select(User.username, User.first_name, User.age, User.gender, User.height, User.weight, User.target)
            users = await session.execute(q)
            return users.all()

    async def get_all_users_telegram_id(self) -> Sequence[User]:
        async with self.session as session:
            session: AsyncSession
            q = select(User.telegram_id_user)
            users = await session.execute(q)
            return users.all()

    async def create_user(self, data: FSMContextProxy) -> User:
        async with self.session as session:
            session: AsyncSession
            user = User(
                telegram_id_user=data['telegram_id'], first_name=data['first_name'],
                username=data['username'], age=data['age'], gender=data['gender'],
                weight=data['weight'], height=data['height'], target=data['target']
            )
            session.add(user)
            await session.commit()
            return user
        
    async def update_user(self, data: FSMContextProxy, telegram_id: Optional[str] = None, user: Optional[User] = None) -> User:
        if not telegram_id and not user:
            raise ValueError('You need to pass: <user> or <telegram_id>')
        if telegram_id and user:
            raise ValueError('You only need to pass one argument: <user> or <telegram_id>')
        async with self.session as session:
            session: AsyncSession
            if telegram_id:
                q = update(User)\
                    .where(User.telegram_id_user == telegram_id)\
                    .values(age=data['age'], gender=data['gender'], weight=data['weight'],
                            height=data['height'], target=data['target'],)
                user = await session.execute(q)
            elif user:
                user.age = data['age']
                user.gender = data['gender']
                user.weight = data['weight']
                user.height = data['height']
                user.target = data['target']
                session.add(user)
            await session.commit()
            return user
        
    async def delete_user(self, telegram_id: str) -> None:
        async with self.session as session:
            session: AsyncSession
            user = await self._get_user(telegram_id=telegram_id)
            await session.delete(user)
            await session.commit()
