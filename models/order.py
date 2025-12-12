from peewee import Model, ForeignKeyField, DateTimeField, AutoField, DecimalField
from .db import db
from .user import User
from .product import Product

class Order(Model):
    id = AutoField() # 注文ごとのID
    user = ForeignKeyField(User, backref='orders') # ユーザID
    product = ForeignKeyField(Product, backref='orders') # 製品ID
    order_date = DateTimeField() # 購入日
    count = DecimalField() # 購入個数

    class Meta:
        database = db
