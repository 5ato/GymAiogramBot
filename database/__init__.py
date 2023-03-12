__all__ = [
    'white_list_gender', 'white_list_age', 'white_list_target',
    'get_engine', 'get_session', 'init_models',
    'User', 'Category', 'Product', 'OrderItem', 'Order',
]

from .tables import User, Category, Product, OrderItem, Order
from .db import get_engine, get_session, init_models


white_list_gender = ['мужчина', 'женщина']
white_list_age = ['13-17', '18-25', '26-35', '36-45', '46+']
white_list_target = ['набрать', 'похудеть', 'быть в форме']
white_list_weight = [
    'меньше 50', '50-55', '56-60', '61-65',
    '66-70', '71-75', '76-80', '81-85',
    '86-90', '91-95', '96-100', '100+',
]
white_list_height = [
    '140-150', '150-160', '160-170', '170-180', '180-190', '190-200', 'более 200см'
]
