from sqlalchemy import Column, Integer, String, DateTime, Boolean
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
    secret_2fa = Column(String)
    status_2fa = Column(Boolean)
