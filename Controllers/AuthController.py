import datetime
import os
from typing import Optional

import pyotp
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from OAuthandJwt.JWTToken import create_jwt
from Models import User
from Database import get_db
from OAuthandJwt.oauth_config import google_oauth
from Schema import StudentSchema, AuthorSchema
from Schema.AuthSchema import Token
from Models.Student import Student as StudentModel
from Schema.StudentSchema import StudentResponse
from Models.Author import Author as AuthorModel
from TwoFAgoogle.SecretandQRCode import generate_2fa_secret, generate_qrcode

app = FastAPI()
AuthRouter = APIRouter(tags=["Auth"])

@AuthRouter.get("/register_via_google")
async def register(request: Request):
    try:
        redirect_uri = os.getenv("REDIRECT_URI")
        if not redirect_uri:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Redirect URI not configured"
            )
        return await google_oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as ex:
        code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex

        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )

@AuthRouter.get("/callback", response_model=Token)
async def callback(request: Request, db : Session = Depends(get_db)):
    try:
        token = await google_oauth.google.authorize_access_token(request)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch access token"
            )

        user_info = token["userinfo"]
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch user info"
            )

        user = db.query(User).filter(User.google_id == user_info['sub']).first()
        if user.secret_2fa is None:
            secret, otp_uri = generate_2fa_secret(user.email)
            qr_code = generate_qrcode(otp_uri)
            user.secret_2fa = secret
            db.commit()
            db.refresh(user)

        if not user:
            role = "Student"
            if user_info['email'].endswith(f"@{os.getenv("ADMIN_EMAILS", '')}"):
                role = "Admin"
            elif user_info['email'].endswith(f"@{os.getenv('AUTHOR_EMAILS', '')}"):
                role = "Author"

            secret, otp_uri = generate_2fa_secret(user_info['email'])
            qr_code = generate_qrcode(otp_uri)

            user = User(
                google_id=user_info['sub'],
                name=user_info['name'],
                email=user_info['email'],
                picture=user_info['picture'],
                user_created_at = datetime.datetime.now(),
                role = role,
                secret_2fa = secret,
                status_2fa = True
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        token = create_jwt({"email": user.email, "name" : user.name, "role": user.role, "from_project": "OAuth2.0 FastAPI"})
        return {"access_token" : token , "token_type" : "bearer" }
    except Exception as ex:
        code=getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex

        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )
    finally:
        db.close()

@AuthRouter.post("/register_manually_Student", response_model=StudentSchema.StudentResponse)
async def register_student(
        request: StudentSchema.StudentCreate,
        db: Session = Depends(get_db)
):
    try:
        check_email = db.query(StudentModel).filter(StudentModel.email == request.email).first()
        secret, otp_uri = generate_2fa_secret(request.email)
        qr_code = generate_qrcode(otp_uri)

        if check_email:
            if check_email.secret_2fa is None:
                check_email.secret_2fa = secret
                db.commit()
                db.refresh(check_email)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        registered_student = StudentModel(**request.model_dump(), secret_2fa = secret , status_2fa = True)
        db.add(registered_student)
        db.commit()
        db.refresh(registered_student)

        token = create_jwt({
            "email": registered_student.email,
            "name": registered_student.name,
            "role" : "Student",
            "from_project": "OAuth2.0 FastAPI"
        })

        std_response = StudentResponse(
            id=registered_student.id,
            name=registered_student.name,
            email=registered_student.email,
            age=registered_student.age,
            IsStudent=registered_student.IsStudent,
            access_token = token,
            qr_code_2fa= qr_code
        )
        return std_response

    except Exception as ex:
        db.rollback()
        if isinstance(ex, HTTPException):
            raise ex

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )
    finally:
        db.close()

@AuthRouter.post('/register_author_manually')
def register_author(requets: AuthorSchema.CreateAuthor, db: Session = Depends(get_db)):
    try:
        if not requets.email.endswith(f"@{os.getenv('AUTHOR_EMAILS', '')}"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Enter email '{requets.email}' not for author registration"
            )

        secret, otp_uri = generate_2fa_secret(requets.email)
        qr_code = generate_qrcode(otp_uri)

        verify_email_exists = db.query(AuthorModel).filter(AuthorModel.email == requets.email).first()
        if verify_email_exists:
            if verify_email_exists.secret_2fa is None:
                verify_email_exists.secret_2fa = secret
                db.commit()
                db.refresh(verify_email_exists)
            raise HTTPException(
                status_code=400,
                detail="Author already registered"
            )

        register_author_model = AuthorModel(**requets.model_dump(), secret_2fa = secret, status_2fa = True)
        db.add(register_author_model)
        db.commit()
        db.refresh(register_author_model)

        token = create_jwt({
            "email": register_author_model.email,
            "name": register_author_model.name,
            "role": "Author",
            "from_project": "OAuth2.0 FastAPI"
        })

        response = jsonable_encoder(register_author_model)
        response.update({
            "token": {
                "access_token": token
            },
            "qr_code":{
                "qr_code_2fa": qr_code
            }
        })

        return response

    except Exception as ex:
        db.rollback()
        code = getattr(500, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex

        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )
    finally:
        db.close()

@AuthRouter.get("/login_via_google", response_model=Token)
def google_login(email: str, otp: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        verify_email = db.query(User).filter(User.email == email).first()
        if not verify_email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entered detail's not found"
            )

        if verify_email.status_2fa is True:
            verif_top = pyotp.TOTP(verify_email.secret_2fa)
            if not verif_top.verify(otp):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid OTP code"
                )
        elif verify_email.status_2fa is False:
            token = create_jwt({
                "email": verify_email.email,
                "name": verify_email.name,
                "role": verify_email.role,
                "from_project": "OAuth2.0 FastAPI"
            })
            return Token(
                access_token=token,
                token_type="bearer"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="2FA not enabled"
            )

        token = create_jwt({
            "email": verify_email.email,
            "name": verify_email.name,
            "role": verify_email.role,
            "from_project": "OAuth2.0 FastAPI"
        })
        return Token(
            access_token=token,
            token_type="bearer"
        )
    except Exception as ex:
        code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex

        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )

@AuthRouter.get("/login", response_model=Token)
def login(email : str, otp: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        get_email = email.endswith(f"{os.getenv('AUTHOR_EMAILS', '')}")
        if get_email:
            verify_author_email = db.query(AuthorModel).filter(AuthorModel.email == email).first()
            if not verify_author_email:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Entered details not found anywhere"
                )
            new_email = verify_author_email.email
            name = verify_author_email.name
            role = "Author"

            if verify_author_email.status_2fa is True:
                totp = pyotp.TOTP(verify_author_email.secret_2fa)
                if not totp.verify(otp):
                    raise HTTPException(status_code=400, detail="Invalid OTP code")

        elif not get_email:
            verify_student_email = db.query(StudentModel).filter(StudentModel.email == email).first()
            if not verify_student_email:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Entered details not found anywhere"
                )
            new_email = verify_student_email.email
            name = verify_student_email.name
            role = "Student"

            if verify_student_email.status_2fa is True:
                totp = pyotp.TOTP(verify_student_email.secret_2fa)
                if not totp.verify(otp):
                    raise HTTPException(status_code=400, detail="Invalid OTP code")

        else:
            raise HTTPException(
                status_code=400,
                detail="Entered details not found anywhere"
            )

        token = create_jwt({
            "email": new_email,
            "name": name,
            "role": role,
            "from_project": "OAuth2.0 FastAPI"})

        return Token(
            access_token = token,
            token_type= "bearer"
        )
    except Exception as ex:
        code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex

        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )
