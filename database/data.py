from peewee import *


my_db = SqliteDatabase('my_data_base.db')


class BaseModel(Model):
    class Meta:
        database = my_db


class User(BaseModel):
    id_user = IntegerField(primary_key=True)
    name = CharField(null=True)
    polity_city = CharField(null=True)
    longitude_adress = CharField(null=True)
    latitude_adress = CharField(null=True)


class History(BaseModel):
    id_user = IntegerField()
    start = CharField()
    stop = CharField()
    date = CharField()
    transport = CharField()
    result = CharField()
    search_parameter = CharField()
    date_search = CharField()


def create_models() -> None:
    my_db.create_tables([User])
    my_db.create_tables([History])



