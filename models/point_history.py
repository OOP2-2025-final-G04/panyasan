from peewee import Model, ForeignKeyField, IntegerField, DateTimeField
from datetime import datetime
from .db import db
from .user import User


class PointHistory(Model):
    user = ForeignKeyField(User, backref='point_histories', on_delete='CASCADE')
    used_point = IntegerField()
    used_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
