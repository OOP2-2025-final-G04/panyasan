from peewee import Model, CharField, DecimalField, AutoField
from .db import db

class Product(Model):
    id = AutoField()
    name = CharField()
    price = DecimalField()
    
    class Meta:
        database = db