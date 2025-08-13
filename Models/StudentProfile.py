from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from Database import Base


class StudentProfile(Base):
    __tablename__ = 'student_profile'

    id = Column(Integer, primary_key=True)
    address = Column(String)
    phone_number = Column(Integer)
    dob = Column(Date)

    student_id = Column(Integer, ForeignKey('students.id'), unique=True)

    student = relationship("Student", back_populates="student_profile")