from datetime import datetime

from pydantic import BaseModel, Json, Field


class CreateBook(BaseModel):
    title : str
    description : str
    author_id : int = Field(alias="authorId")
    year : int

class ResponseCreateBook(BaseModel):
    id : int
    title : str
    description : str
    year: int
    author_id : int

class AssignBookToStudent(BaseModel):
    book_id : int
    book_title : str = Field(alias="title")
    student_id : int
    student_email : str = Field(alias="email")

class ResponseAssignBookToStudent(BaseModel):
    name : str = Field(alias="Student_Name")
    email : str = Field(alias="Student_Email")
    title : str = Field(alias="Book_Title")
    author : str = Field(alias="Book_Author")
    AssignedAt : datetime


class ReturnBook(BaseModel):
    book_title: str = Field(alias="title")
    student_email: str = Field(alias="email")
