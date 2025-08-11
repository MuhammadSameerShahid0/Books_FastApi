from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from Database import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    bio = Column(String)
    nationality = Column(String)

    # Establish relationship
    books = relationship("Book", back_populates="author")