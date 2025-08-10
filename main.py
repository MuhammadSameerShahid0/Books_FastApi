from fastapi import FastAPI

from StudentController import Books

app = FastAPI()

app.include_router(Books)