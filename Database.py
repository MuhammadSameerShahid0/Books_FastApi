from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

class Database:
    __instance = None

    #__new__ is a special method that controls object creation (before __init__).
    def __new__(cls, db_url = 'postgresql://postgres:1234@localhost:5432/FastApi'):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.create_engine = create_engine(db_url)
            cls.__instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= cls.__instance.create_engine)
            cls.__instance.Base = declarative_base()
        return cls.__instance

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_table(self):
        self.Base.metadata.create_all(bind=self.create_engine)

db_singleton = Database()

Base = db_singleton.Base

def get_db():
    yield from db_singleton.get_db()


#---Classic Singleton with Decorator---

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
#
# def singleton(cls):
#     instances = {}
#     def get_instance(*args, **kwargs):
#         if cls not in instances:
#             instances[cls] = cls(*args, **kwargs)
#         return instances[cls]
#     return get_instance
#
# @singleton
# class Database:
#     def __init__(self, db_url='postgresql://postgres:1234@localhost:5432/FastApi'):
#         self.engine = create_engine(db_url)
#         self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
#         self.Base = declarative_base()
#
#     def get_db(self):
#         db = self.SessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()
#
#     def create_table(self):
#         self.Base.metadata.create_all(bind=self.engine)
#
# # Usage
# db_singleton = Database()
# Base = db_singleton.Base
