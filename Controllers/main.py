from fastapi import FastAPI

from Controllers.BooksController import Books
from Controllers.StudentController import Student

app = FastAPI()

app.include_router(Student)
app.include_router(Books)