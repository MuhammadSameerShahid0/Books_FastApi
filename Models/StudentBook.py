from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from Database import Base


class StudentBook(Base):
    __tablename__ = 'student_books'

    id = Column(Integer, primary_key=True)
    AssignedAt = Column(DateTime)
    ReturnDate = Column(DateTime)
    Status = Column(String)
    student_id = Column(Integer, ForeignKey('students.id'))
    book_id = Column(Integer, ForeignKey('books.id'))

    # Relationships
    student = relationship("Student", back_populates="student_books")
    book = relationship("Book", back_populates="book_students")