# coding: utf-8

from peewee import *
from config import db_file
import datetime

db = SqliteDatabase(db_file)


class Climat(Model):
    date = DateTimeField(unique=True, verbose_name="Дата")
    temp = FloatField(unique=False, verbose_name="Температура")
    hum = FloatField(unique=False, verbose_name="Влажность")
    pres = FloatField(unique=False, verbose_name="Давление")
    lux = FloatField(unique=False, verbose_name="Освещенность")
    
    class Meta:
        database = db


db.create_tables([
    Climat
])


def save_to_base(data):
    cl = Climat(
        date=datetime.datetime.now(),
        temp=data.get('temp'),
        hum=data.get('hum'),
        pres=data.get('pres'),
        lux=data.get('lux'),
    )
    cl.save()
    return 0


def get_last_row():
    last_record = Climat.select().order_by(Climat.id.desc()).get()
    return last_record
