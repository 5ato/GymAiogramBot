from aiogram import types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from database import white_list_gender
from .start import FSMRegistration
from services import AuthService
import commands

import logging


async def profile(message: types.Message) -> None:
    menu = commands.get_menu()
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    
    logging.info(user)

    if user:
        await message.answer(
            f'<b>Вес</b>:  {user.weight}\n'\
            f'<b>Рост</b>:  {user.height}\n'\
            f'<b>Возраст</b>:  {user.age}\n'\
            f'<b>Пол</b>:  {user.gender}\n'\
            f'<b>Цель</b>:  {user.target}',
            reply_markup=menu, parse_mode='HTML'
        )
    else:
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        menu.add(KeyboardButton(text='Начать регистрацию'))

        await message.answer(
            'Для общения с ботом нужна регистрация', reply_markup=menu
        )
        await commands.FSMRegistration.wait_confirmation_state.set()


async def update_profile(message: types.Message) -> None:
    choice_gender = ReplyKeyboardMarkup(resize_keyboard=True)
    for gender in white_list_gender:
        choice_gender.add(KeyboardButton(text=gender.capitalize()))
    await message.answer(text='Выберете ваш пол', parse_mode='HTML', reply_markup=choice_gender)
    await FSMRegistration().wait_gender_state.set()
