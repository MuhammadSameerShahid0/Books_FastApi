
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

# 8 Alembic Tutorial
https://www.youtube.com/watch?v=zy8ZIAhl_fM&ab_channel=Knowbasiks

# 8.1 Alembic for migrations
alembic init alembic

# 8.2 Migrations 
alembic revision --autogenerate -m "updated lib in env"
alembic upgrade head 
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

## 🔥 Database
```bash
# Database.py (File need to Create)

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
    
# env.py in alembic folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
(Create the another file **__init__.py** and import all lib in this class)
> from Models import * 
> target_metadata = Base.metadata

#alembic.ini (update the url)
> sqlalchemy.url = postgresql://postgres:1234@localhost:5432/FastApi
```
## 🧠 What is Pydantic 
```bash
> ✅ Pydantic = Validation + Parsing using Python types
> 🧠 Used for request/response models in FastAPI
> 🔒 Helps you catch errors early with strict type checking
```
## 🔑 Google OAuth 2.0 + JWT Authentication Setup
```bash
---Packages---

itsdangerous
httpx
authlib
python-dotenv
PyJWT

📄.env Configuration
Create a .env file in the project root:

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

SECRET_KEY=super_secret_change_me
JWT_EXPIRE_SECONDS=3600

📝 Replace your_google_client_id and your_google_client_secret with credentials 
from the Google Cloud Console.

---Middleware---

load_dotenv()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)
```

## 🔑 2FA Google
```bash
--packages--
pyotp
qrcode[PIL]
Pillow

def generate_2fa_secret(email: str):
    secret = pyotp.random_base32()
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="BooksCRUD_FastApi")
    return secret, otp_uri

def generate_qrcode(opt_uri: str):
    try:
        qr = qrcode.make(opt_uri)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")  # Use a string literal for the format
        qr_buffer = buffer.getvalue()
        response = base64.b64encode(qr_buffer).decode("utf-8")
        return response
    except Exception as ex:
        return {"Error": str(ex)}
        
--Use this in endpoints--
 secret, otp_uri = generate_2fa_secret(requets.email)
qr_code = generate_qrcode(otp_uri)
        
---Verify Otp---
totp = pyotp.TOTP(verify_author_email.secret_2fa)
        if not totp.verify(otp):
            raise HTTPException(
                status_code=400,
                detail="Invalid OTP code"
            )
```