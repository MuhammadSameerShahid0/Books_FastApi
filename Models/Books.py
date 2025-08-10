from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from Database import Base
from Models.StudentBook import StudentBook


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    year = Column(Integer)

    # Association proxy to get students directly
    students = association_proxy("book_students", "students")

    # Relationship to association class
    book_students = relationship("StudentBook", back_populates="book")
