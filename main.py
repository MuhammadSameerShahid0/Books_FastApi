from fastapi import FastAPI

from BooksController import Books
from StudentController import Student

app = FastAPI()

app.include_router(Student)
app.include_router(Books)