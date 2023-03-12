__all__ = ['bot_commands', 'bot_set_commands', 'register_user_commands', 'get_menu', 'FSMRegistration']

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import BotCommand
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from .start import (
    start, FSMRegistration,
    fsm_gender, fsm_age, fsm_weight, fsm_height, fsm_target, fsm_confirmation
)
from .products import view_product, start_viewing, FSMViewProduct
from .help import help_command, help_help
from .profile import profile, update_profile
from .location import get_location
from .admin import (
    all_users, cancel,
    set_location, start_set_location, FSMAdminSetLocation,
    get_all_category, create_category, start_create_category, FSMAdminCategory,
    start_create_product, fsm_name, fsm_price, fsm_description, fsm_image, fsm_category, FSMAdminProduct,
    send_all_restart
)
from database import (
    white_list_gender, white_list_age, white_list_target,
    white_list_height, white_list_weight
)


def get_menu() -> ReplyKeyboardMarkup:
    menu = ReplyKeyboardMarkup(resize_keyboard=True)\
           .row(KeyboardButton('Профиль'), KeyboardButton('Изменить профиль'))\
           .row(KeyboardButton('Помощь'), KeyboardButton('Местоположение спортзала'))\
           .add(KeyboardButton('Посмотреть товары'))
    return menu


bot_commands = (
    ('start', 'Активация бота', 'Команда для активации бота'),
    ('help', 'Справка о командах', 'Описание и инструкция о командах бота'),
    ('profile', 'Показать профиль', 'Показывает вашу подробую информацию'),
    ('location', 'Местоположеие спортзала', 'Показывает местоположение спортзала'),
)


bot_set_commands = [BotCommand(command[0], command[1]) for command in bot_commands]


def register_user_commands(dp: Dispatcher):

    dp.register_message_handler(start, Command(commands=['start']))

    dp.register_message_handler(send_all_restart, Command(commands=['admin_send_all_restart']))

    dp.register_message_handler(profile, lambda msg: msg.text.lower() == 'профиль')
    dp.register_message_handler(profile, Command(commands=['profile']))

    dp.register_message_handler(get_all_category, Command(commands=['admin_get_all_category']))
    dp.register_message_handler(start_create_category, Command(commands=['admin_create_category']))
    dp.register_message_handler(create_category, state=FSMAdminCategory.wait_category_state)

    dp.register_message_handler(start_set_location, Command(commands=['admin_set_location']))
    dp.register_message_handler(
        set_location,
        content_types=['location'],
        state=FSMAdminSetLocation.wait_location_state
    )
    dp.register_message_handler(get_location, Command(commands=['location']))
    dp.register_message_handler(get_location, lambda msg: msg.text.lower() == 'местоположение спортзала')

    dp.register_message_handler(cancel, lambda msg: msg.text.lower() == 'отмена', state='*')
    dp.register_message_handler(cancel, lambda msg: msg.text.lower() == 'отменить просмотр', state='*')

    dp.register_message_handler(start_viewing, lambda msg: msg.text.lower() == 'посмотреть товары')
    dp.register_message_handler(
        view_product,
        lambda msg: msg.text.lower() == 'начать',
        state=FSMViewProduct.wait_product_state
    )
    dp.register_message_handler(
        view_product,
        lambda msg: msg.text.lower() == 'пропустить',
        state=FSMViewProduct.wait_product_state
    )

    dp.register_message_handler(start_create_product, Command(commands=['admin_create_product']))
    dp.register_message_handler(
        fsm_name, state=FSMAdminProduct.wait_name_state
    )
    dp.register_message_handler(
        fsm_category, lambda msg: msg.text.isdigit(), state=FSMAdminProduct.wait_category_state
    )
    dp.register_message_handler(
        fsm_price, lambda msg: msg.text.isdigit(), state=FSMAdminProduct.wait_price_state
    )
    dp.register_message_handler(
        fsm_description, state=FSMAdminProduct.wait_description_state
    )
    dp.register_message_handler(
        fsm_image, content_types=['photo'], state=FSMAdminProduct.wait_image_state
    )

    dp.register_message_handler(all_users, Command(commands=['admin_get_all_users']))
    dp.register_message_handler(
        update_profile,
        lambda msg: msg.text.lower() == 'изменить профиль',
    )
    dp.register_message_handler(
        fsm_confirmation,
        lambda msg: msg.text.lower() == 'начать регистрацию',
        state=FSMRegistration.wait_confirmation_state
    )
    dp.register_message_handler(
        fsm_gender,
        lambda msg: msg.text.lower() in white_list_gender,
        state=FSMRegistration.wait_gender_state,
    )
    dp.register_message_handler(
        fsm_age,
        lambda msg: msg.text.lower() in white_list_age,
        state=FSMRegistration.wait_age_state
    )
    dp.register_message_handler(
        fsm_weight,
        lambda msg: msg.text.lower() in white_list_weight,
        state=FSMRegistration.wait_weight_state
    )
    dp.register_message_handler(
        fsm_height,
        lambda msg: msg.text.lower() in white_list_height,
        state=FSMRegistration.wait_height_state
    )
    dp.register_message_handler(
        fsm_target,
        lambda msg: msg.text.lower() in white_list_target,
        state=FSMRegistration.wait_target_state
    )
    dp.register_message_handler(help_command, Command(commands=['help']))
    dp.register_message_handler(help_help, lambda msg: msg.text.lower() == 'помощь')
