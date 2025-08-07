from sqlalchemy import Column, Integer, String
from Database import Base

class Book(Base):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    year = Column(Integer)