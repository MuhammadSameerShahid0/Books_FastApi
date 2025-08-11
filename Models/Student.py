from fastapi.datastructures import Default
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from Database import Base


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)
    IsStudent = Column(Boolean)

    # Association proxy to get books directly
    books = association_proxy("student_books", "books")

    # Relationship to association class
    student_books = relationship("StudentBook", back_populates="student")
