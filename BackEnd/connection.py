import pymysql

from BackEnd.config import database

def connect_db():
    return pymysql.connect(
        host    = database['host'],
        port    = database['port'],
        user    = database['user'],
        passwd  = database['passwd'],
        db      = database['db'],
        charset = database['charset']
    )