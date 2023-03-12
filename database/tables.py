from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects import postgresql as sql
from sqlalchemy import Column, ForeignKey, DateTime

from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(sql.INTEGER, primary_key=True, autoincrement=True)
    telegram_id_user = Column(sql.VARCHAR(30), nullable=False)
    first_name = Column(sql.VARCHAR(86), nullable=True)
    username = Column(sql.VARCHAR(86), nullable=True)
    age = Column(sql.VARCHAR(10), nullable=False)
    gender = Column(sql.VARCHAR(10), nullable=False)
    weight = Column(sql.VARCHAR(10), nullable=False)
    height = Column(sql.VARCHAR(20), nullable=False)
    target = Column(sql.VARCHAR(20), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    is_bot = Column(sql.BOOLEAN, default=False, nullable=False)
    is_superuser = Column(sql.BOOLEAN, default=False, nullable=False)

    created_products_user = relationship('Product', back_populates='user_created')
    orders = relationship('Order', back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(sql.INTEGER, primary_key=True, autoincrement=True)
    name = Column(sql.VARCHAR(86), nullable=False)

    products_cat = relationship('Product', back_populates='category')


class OrderItem(Base):
    __tablename__ = 'orderitems'

    product_id = Column(
        sql.INTEGER,
        ForeignKey('products.id'),
        primary_key=True,
        nullable=False,
    )
    order_id = Column(
        sql.INTEGER,
        ForeignKey('orders.id'),
        primary_key=True,
        nullable=False
    )


class Product(Base):
    __tablename__ = 'products'

    id = Column(sql.INTEGER, primary_key=True, autoincrement=True)
    name = Column(sql.VARCHAR(256), nullable=False)
    prcie = Column(sql.INTEGER, nullable=False)
    description = Column(sql.TEXT, nullable=True)
    image = Column(sql.TEXT, nullable=False)

    user_id_created = Column(sql.INTEGER, ForeignKey('users.id'), nullable=False)
    category_id = Column(sql.INTEGER, ForeignKey('categories.id'), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship('Category', back_populates='products_cat')
    user_created = relationship('User', back_populates='created_products_user')
    orders = relationship('Order', secondary='orderitems', back_populates='products')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(sql.INTEGER, primary_key=True, autoincrement=True)
    date_created_order = Column(DateTime, default=datetime.utcnow)

    user_id = Column(sql.INTEGER, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='orders')
    products = relationship('Product', secondary='orderitems', back_populates='orders')
