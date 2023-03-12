from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup

from services import AuthService, CategoryService, ProductService
import commands

import json
import logging


class FSMAdminSetLocation(StatesGroup):
    wait_location_state = State()


class FSMAdminCategory(StatesGroup):
    wait_category_state = State()


class FSMAdminProduct(StatesGroup):
    wait_name_state = State()
    wait_category_state = State()
    wait_price_state = State()
    wait_description_state = State()
    wait_image_state = State()


async def all_users(message: types.Message) -> None:
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user.is_superuser:
        session = message.bot.get('db')
        service = AuthService(session=session)
        users = await service.get_all_users()
        logging.info(users)
        for user in users:
            await message.answer(
                f'{user.username}, {user.first_name}, {user.age}, {user.gender}, {user.weight}, {user.height}, {user.target}'
            )
    else:
        await message.answer('У вас нету прав')


async def start_set_location(message: types.Message) -> None:
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user.is_superuser:
        menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        menu.row(KeyboardButton('Отправить локацию', request_location=True), KeyboardButton('Отмена'))
        await message.answer('Отправте свою геопозицию для фиксации спортзала', reply_markup=menu)
        await FSMAdminSetLocation.wait_location_state.set()
    else:
        await message.answer('У вас нету прав')


async def set_location(message: types.Message, state: FSMContext) -> None:
    lat = message.location.latitude
    lon = message.location.longitude
    coordinate = {'lat': lat, 'lon': lon}
    with open('CourseBot/location.json', 'w', encoding='utf-8') as file:
        json.dump(coordinate, file, indent=4, ensure_ascii=False)
    await message.answer('Геопозиция сохранена')
    await state.finish()


async def cancel(message: types.Message, state: FSMContext) -> None:
    menu = commands.get_menu()
    await message.answer('Произошла отмена', reply_markup=menu)
    await state.finish()


async def get_all_category(message: types.Message) -> None:
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user.is_superuser:
        session = message.bot['db']
        service = CategoryService(session=session)
        categories = await service.get_all_category()
        for category in categories:
            await message.answer(text=f'{category.name}')
    else:
        await message.answer('У вас нету прав')


async def start_create_category(message: types.Message) -> None:
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user.is_superuser:
        await message.answer('Напишите категорию(автоматически переводится в нижний регистер)')
        await FSMAdminCategory.wait_category_state.set()
    else:
        await message.answer('У вас нету прав')


async def create_category(message: types.Message, state: FSMContext) -> None:
    session = message.bot['db']
    service = CategoryService(session=session)
    await service.create_category(name=message.text.lower())
    await message.answer(f'Категория |{message.text.capitalize()}| успшено добавлена')
    await state.finish()


async def start_create_product(message: types.Message) -> None:
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user.is_superuser:
        await message.answer('Введите название продукта(Всё автоматически переводится в нижний регистр)')
        await FSMAdminProduct.wait_name_state.set()
    else:
        await message.answer('У вас нету прав')


async def fsm_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        session = message.bot['db']
        service = CategoryService(session=session)
        categoryies = await service.get_all_category()
        for key, item in enumerate(categoryies):
            await message.answer(text=f'{key+1}|-----------|{item.name.capitalize()}')
            menu.add(KeyboardButton(text=key+1))
        

        data['name'] = message.text.lower()
        await message.answer('Нажмите на кпопку чтобы выбрать категорию', reply_markup=menu)
        await state.set_state(FSMAdminProduct.wait_category_state)


async def fsm_category(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        async with state.proxy() as data:
            data['category_id'] = int(message.text)
            await message.answer('Введите цену товара(только числа)')
            await state.set_state(FSMAdminProduct.wait_price_state)
    else:
        await message.answer('Нажмите только на кнопки')


async def fsm_price(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit:
        async with state.proxy() as data:
            data['price'] = int(message.text)
            await message.answer('Опишите ваш продукт(описание)')
            await state.set_state(FSMAdminProduct.wait_description_state)
    else:
        await message.answer('Неверный ввод')


async def fsm_description(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
        await message.answer('Пришлите изображение товара')
        await state.set_state(FSMAdminProduct.wait_image_state)


async def fsm_image(message: types.Message, state: FSMContext) -> None:
    if message.content_type == ContentType.PHOTO:
        async with state.proxy() as data:
            session = message.bot['db']
            product_service = ProductService(session=session)
            user_service = AuthService(session=session)
            user = await user_service.get_user(str(message.from_user.id))
            data['image'] = message.photo[0].file_id
            data['user_id_created'] = user.id
            await product_service.create_product(data=data)
            await message.answer('Вы успешно добавили продукт')
            await state.finish()
    else:
        await message.answer('Пришлите изображение')


async def send_all_restart(message: types.Message) -> None:
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user.is_superuser:
        session = message.bot.get('db')
        service = AuthService(session=session)
        users_telegram_id = await service.get_all_users_telegram_id()
        for user in users_telegram_id:
            await message.bot.send_message(
                chat_id=int(user.telegram_id_user),
                text='Для общения с ботом, нужно его перезапустить',
                reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='/start'))
            )
        await message.answer('Отправлено!')
    else:
        await message.answer('У вас нету прав')