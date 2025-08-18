from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import os
from Controllers.AuthController import AuthRouter
from Controllers.AuthorController import Author
from Controllers.BooksController import Books
from Controllers.CompleteStdDetailsController import CompleteStdDetails
from Controllers.Google2FAController import Google2FA
from Controllers.StudentController import Student
from Controllers.StudentProfileController import StudentProfiles

load_dotenv()

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),  # must be secure in production
)

app.include_router(Student)
app.include_router(Books)
app.include_router(Author)
app.include_router(StudentProfiles)
app.include_router(CompleteStdDetails)
app.include_router(AuthRouter)
app.include_router(Google2FA)