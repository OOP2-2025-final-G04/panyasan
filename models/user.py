from peewee import Model, CharField, IntegerField,DateField,AutoField
from .db import db

class User(Model):
    name = CharField()
    point = IntegerField(default=0)
    birth_date = DateField()
    id = AutoField(primary_key=True)
    gender = CharField(choices=[("M", "男性"), ("F", "女性"), ("O", "その他")])
    age = IntegerField()
    
    class Meta:
        database = db