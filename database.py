import os
from sqlite3 import Connection, connect

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

base_dir = os.path.dirname(__file__)
db_path = os.path.join(base_dir, 'movies.db')

SQLALCHEMY_DATABASE_URL = f'sqlite:///{db_path}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def getdb():
    with SessionLocal() as db:
        yield db


def sqlite_connect() -> Connection:
    conn = connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn