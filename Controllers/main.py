from fastapi import FastAPI

from Controllers.AuthorController import Author
from Controllers.BooksController import Books
from Controllers.StudentController import Student
from Controllers.StudentProfileController import StudentProfiles

app = FastAPI()

app.include_router(Student)
app.include_router(Books)
app.include_router(Author)
app.include_router(StudentProfiles)