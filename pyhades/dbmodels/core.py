from peewee import Proxy, Model

proxy = Proxy()

SQLITE = 'sqlite'
MYSQL = 'mysql'
POSTGRESQL = 'postgresql'


class BaseModel(Model):
    class Meta:
        database = proxy