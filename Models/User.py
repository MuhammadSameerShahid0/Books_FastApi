from sqlalchemy import Column, Integer, String, DateTime
from Database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    google_id = Column(String, unique=True)
    email = Column(String, unique=True)
    name = Column(String)
    picture = Column(String)
    user_created_at = Column(DateTime)
    role = Column(String , default="Student")
