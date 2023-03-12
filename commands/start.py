from aiogram import types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import logging

import commands
from database import (
    white_list_gender, white_list_age,
    white_list_target, white_list_weight,
    white_list_height,
)
from services import AuthService


class FSMRegistration(StatesGroup):
    wait_confirmation_state = State()
    wait_gender_state = State()
    wait_age_state = State()
    wait_weight_state = State()
    wait_height_state = State()
    wait_target_state = State()


async def start(message: types.Message) -> None:
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_user.id))
    if not user:
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        menu.add(KeyboardButton(text='Начать регистрацию'))


        await message.answer(
            'Для общения с ботом нужно зарегистрироваться', reply_markup=menu
        )
        await FSMRegistration.wait_confirmation_state.set()
    else:
        menu = commands.get_menu()
        await message.answer(
            text='Выберете и нажмите на любую вам нужную кнопку',
            reply_markup=menu
        )


async def fsm_confirmation(message: types.Message, state: FSMContext) -> None:
    choice_gender = ReplyKeyboardMarkup(resize_keyboard=True)
    for gender in white_list_gender:
        choice_gender.add(KeyboardButton(text=gender.capitalize()))
    

    async with state.proxy() as data:
        data['telegram_id'] = str(message.from_user.id)
        data['id_bot'] = message.from_user.is_bot
        data['first_name'] = message.from_user.first_name
        data['username'] = message.from_user.username if message.from_user.username else None

    await message.answer(text='Выберете ваш пол', parse_mode='HTML', reply_markup=choice_gender)
    await state.set_state(FSMRegistration.wait_gender_state)


async def fsm_gender(message: types.Message, state: FSMContext) -> None:
    choice_age = ReplyKeyboardMarkup(resize_keyboard=True)

    for age in white_list_age:
        choice_age.add(KeyboardButton(text=age.capitalize()))

    if message.text.lower() in white_list_gender:
        async with state.proxy() as data:
            data['gender'] = message.text
            await message.answer(text='Выберете ваш возраст', parse_mode='HTML', reply_markup=choice_age)
            await state.set_state(FSMRegistration.wait_age_state)


async def fsm_age(message: types.Message, state: FSMContext) -> None:
    choice_weight = ReplyKeyboardMarkup(resize_keyboard=True)

    choice_weight.row(
        KeyboardButton(text='Меньше 50'), KeyboardButton(text='50-55'), KeyboardButton(text='56-60'), KeyboardButton(text='61-65')
    )
    choice_weight.row(
        KeyboardButton(text='66-70'), KeyboardButton(text='71-75'), KeyboardButton(text='76-80'), KeyboardButton(text='81-85')
    )
    choice_weight.row(
        KeyboardButton(text='86-90'), KeyboardButton(text='91-95'), KeyboardButton(text='96-100'), KeyboardButton(text='100+')
    )

    if message.text in white_list_age:
        async with state.proxy() as data:
            data['age'] = message.text
            await message.answer(text='Выберете ваш вес', parse_mode='HTML', reply_markup=choice_weight)
            await state.set_state(FSMRegistration.wait_weight_state)


async def fsm_weight(message: types.Message, state: FSMContext) -> None:
    choice_height = ReplyKeyboardMarkup(resize_keyboard=True)

    choice_height.row(
        KeyboardButton(text='140-150'), KeyboardButton(text='150-160'), KeyboardButton(text='160-170')
    )
    choice_height.row(
        KeyboardButton(text='170-180'), KeyboardButton(text='180-190'), KeyboardButton(text='190-200')
    )
    choice_height.add(KeyboardButton(text='Более 200см'))

    if message.text.lower() in white_list_weight:
        async with state.proxy() as data:
            data['weight'] = message.text
            await message.answer('Выберете ваш рост', reply_markup=choice_height)
            await state.set_state(FSMRegistration.wait_height_state)


async def fsm_height(message: types.Message, state: FSMContext) -> None:
    choice_target = ReplyKeyboardMarkup(resize_keyboard=True)

    choice_target.row(KeyboardButton(text='Набрать'), KeyboardButton(text='Быть в форме'))
    choice_target.add(KeyboardButton(text='Похудеть'))

    if message.text.lower() in white_list_height:
        async with state.proxy() as data:
            data['height'] = message.text
            await message.answer('Выберете свою цель', reply_markup=choice_target)
            await state.set_state(FSMRegistration.wait_target_state)


async def fsm_target(message: types.Message, state: FSMContext) -> None:
    if message.text.lower() in white_list_target:
        session = message.bot.get('db')
        service = AuthService(session=session)
        user = await service.get_user(str(message.from_user.id))
        menu = commands.get_menu()
        async with state.proxy() as data:
            data['target'] = message.text.lower()
            if not user:
                await message.answer('Регистрация успешно пройдена', reply_markup=menu)
                await service.create_user(data)
            else:
                await message.answer('Вы успешно обновили свой профиль', reply_markup=menu)
                await service.update_user(user=user, data=data)
            await state.finish()
