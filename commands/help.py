from aiogram import types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Command

from services import AuthService
import commands


async def help_command(message: types.Message, command: Command.CommandObj) -> None:
    menu = commands.get_menu()
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user:
        if command.args:
            for exsist_command in commands.bot_commands:
                if command.args == exsist_command[0]:
                    return await message.answer(
                        f'{exsist_command[0]} -- {exsist_command[1]}\n{exsist_command[2]}',
                        reply_markup=menu
                    )
            return await message.answer(f'{command.args} -- Команда не найдена', reply_markup=menu)
        return await help_help(message)
    else:
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        menu.add(KeyboardButton(text='Начать регистрацию'))

        await message.answer(
            'Для общения с ботом нужна регистрация'
        )
        await commands.FSMRegistration.wait_confirmation_state.set()


async def help_help(message: types.Message) -> None:
    session = message.bot.get('db')
    service = AuthService(session=session)
    user = await service.get_user(str(message.from_id))
    if user:
        menu = commands.get_menu()
        return await message.answer(
            'Помощь и справка о боте\nДля того чтобы получить иформацию о команде, используй /help | командa |\n'\
            '<b>Пример: </b>/help profile',
            parse_mode='HTML',
            reply_markup=menu
        )
    else:
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        menu.add(KeyboardButton(text='Начать регистрацию'))

        await message.answer(
            'Для общения с ботом нужна регистрация'
        )
        await commands.FSMRegistration.wait_confirmation_state.set()
