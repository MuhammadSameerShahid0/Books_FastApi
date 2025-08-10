from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from Database import Base


class StudentBook(Base):
    __tablename__ = 'student_books'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)

    # Relationships
    student = relationship("Student", back_populates="student_books")
    book = relationship("Book", back_populates="book_students")