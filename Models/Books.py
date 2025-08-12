from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from Database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    year = Column(Integer)

    #region Many-to-Many Relationship StudentBook

    # Association proxy to get students directly
    students = association_proxy("book_students", "students")

    # Relationship to association class
    book_students = relationship("StudentBook", back_populates="book")
    #endregion

    #region 1-to-Many Relationship Author

    # Add foreign key to Author
    author_id = Column(Integer, ForeignKey('authors.id'))
    # Establish relationship
    author = relationship("Author", back_populates="books")

    #endregion
