from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup

from services import ProductService, AuthService
import commands

import logging


class FSMViewProduct(StatesGroup):
    wait_product_state = State()


async def start_viewing(message: Message) -> None:
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user:
        await message.answer(
            text='Сейчас вам по очерёдности будут появляться наши товары',
            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Начать')).add(KeyboardButton('Отмена'))
        )
        await FSMViewProduct.wait_product_state.set()
    else:
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        menu.add(KeyboardButton(text='Начать регистрацию'))

        await message.answer(
            'Для общения с ботом нужна регистрация'
        )
        await commands.FSMRegistration.wait_confirmation_state.set()


async def view_product(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if data.get('count', None) is None:
            session = message.bot.get('db')
            service = ProductService(session=session)
            products = await service.get_all_products()
            data['products'] = products
            data['count'] = 0
        else:
            data['count'] += 1  

        logging.info(data['count'])
        logging.info(data['products'])

        menu = ReplyKeyboardMarkup(resize_keyboard=True)\
               .add(KeyboardButton(text='Пропустить'))\
               .add(KeyboardButton(text='Купить Товар'))

        await message.answer_photo(
            data['products'][data['count']].image,
            f'<b>Название: </b>{data["products"][data["count"]].name.capitalize()}\n'\
            f'<b>Цена: </b>{data["products"][data["count"]].prcie}\n'\
            f'<b>Описание: </b>{data["products"][data["count"]].description.capitalize()}',
            reply_markup=menu, parse_mode='HTML'
        )

        if data['count'] == len(data['products'])-1:
            menu = commands.get_menu()
            await state.finish()
            await message.answer(
                'Вы просмотрели все товары', reply_markup=menu
            )
        else:
            await state.set_state(FSMViewProduct.wait_product_state)
