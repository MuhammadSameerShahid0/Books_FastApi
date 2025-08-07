
# 🚀 FastAPI Project Setup Using Virtual Environment

This README covers the basic steps to set up a FastAPI project using Python's built-in virtual environment.

---
## 🛠️ Setup Steps

```bash 
# 1. Create the virtual environment
python -m venv venv

# 2. Activate the virtual environment (Windows)
venv\scripts\activate

# 3. Install FastAPI
pip install fastapi

# 4. Install uvicorn to run the fastapi
pip install uvicorn

# 5. Run the app
uvicorn main:app

# 6. AutoChanges Detect in swagger
uvicorn main:app --reload

# 7 Install the packages from txt file
pip install -r Books/requirements.txt
```
## 🔥 Swagger
```bash
FastAPI automatically generates interactive API documentation using Swagger UI.

- 📄 Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- 📘 ReDoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

# Sometimes Swagger giving error that not change the endpoints so use these commands
 => Get-Process -Name "python" 
 => Stop-Process -Name "python" -Force
 => Then close the pycharm and re-open
```

## 🔥 Debug Settings
![img.png](img.png)
```bash
> Install this if still breakpoint not work 
> > (pydevd_pycharm) install this package
```

## 🧠 What is Pydantic 
```bash
> ✅ Pydantic = Validation + Parsing using Python types
> 🧠 Used for request/response models in FastAPI
> 🔒 Helps you catch errors early with strict type checking
```

## 🔥 Database
```bash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1234@localhost:5432/FastApi"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_table():
    Base.metadata.create_all(bind=engine)
```
