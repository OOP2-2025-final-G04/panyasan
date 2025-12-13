from peewee import SqliteDatabase
from .db import db
from .user import User
from .product import Product
from .order import Order
from .point_history import PointHistory

# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    User,
    Product,
    Order,
    PointHistory,
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()