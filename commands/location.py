from aiogram import types 
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from services import AuthService
import commands

import json


async def get_location(message: types.Message) -> None:
    menu = commands.get_menu()
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user:
        with open('CourseBot/location.json', 'r') as file:
            coordinate = json.load(file)
        await message.answer_location(coordinate['lat'], coordinate['lon'], reply_markup=menu)
    else:
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        menu.add(KeyboardButton(text='Начать регистрацию'))

        await message.answer(
            'Для общения с ботом нужна регистрация'
        )
        await commands.FSMRegistration.wait_confirmation_state.set()
