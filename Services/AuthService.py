import datetime
import os
from typing import Optional

import pyotp
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from Interfaces.IAuthService import IAuthService
from Models.User import User as UserModel
from Models.Student import Student as StudentModel
from Models.Author import Author as AuthorModel
from OAuthandJwt.JWTToken import create_jwt
from OAuthandJwt.oauth_config import google_oauth
from Schema import StudentSchema, AuthorSchema
from Schema.AuthSchema import Token
from Schema.StudentSchema import StudentResponse
from TwoFAgoogle.SecretandQRCode import generate_2fa_secret, generate_qrcode
from Interfaces.IEmailService import IEmailService


class AuthService(IAuthService):
    def __init__(self, db: Session, email_service: IEmailService):
        self.db = db
        self.email_service = email_service

    #region Register
    async def google_register(self, request: Request):
        try:
            frontend_redirect_uri = request.query_params.get("frontend_redirect_uri")
            redirect_uri = os.getenv("REDIRECT_URI")

            if not redirect_uri:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Redirect URI not configured"
                )
            request.session["frontend_redirect_uri"] = frontend_redirect_uri

            return await google_oauth.google.authorize_redirect(request, redirect_uri)
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    async def google_callback(self, request: Request):
        try:
            token = await google_oauth.google.authorize_access_token(request)
            if not token or "userinfo" not in token:
                raise HTTPException(status_code=400, detail="Failed to fetch Google user info")

            user_info = token["userinfo"]
            user = self.db.query(UserModel).filter(UserModel.google_id == user_info['sub']).first()
            if user.secret_2fa is None:
                secret, otp_uri = generate_2fa_secret(user.email)
                qr_code = generate_qrcode(otp_uri)
                user.secret_2fa = secret
                self.db.commit()
                self.db.refresh(user)

            if not user:
                role = "Student"
                if user_info['email'].endswith(f"@{os.getenv("ADMIN_EMAILS", '')}"):
                    role = "Admin"
                elif user_info['email'].endswith(f"@{os.getenv('AUTHOR_EMAILS', '')}"):
                    role = "Author"

                secret, otp_uri = generate_2fa_secret(user_info['email'])
                qr_code = generate_qrcode(otp_uri)

                user = UserModel(
                    google_id=user_info['sub'],
                    name=user_info['name'],
                    email=user_info['email'],
                    picture=user_info['picture'],
                    user_created_at=datetime.datetime.now(),
                    role=role,
                    secret_2fa=secret,
                    status_2fa=True
                )

                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)

                token = create_jwt(
                {
                    "email": user.email,
                    "name": user.name,
                    "role": user.role,
                    "from_project": "OAuth2.0 FastAPI"
                })

            frontend_redirect_uri = request.session.get("frontend_redirect_uri")
            if frontend_redirect_uri:
                # Redirect to frontend with token as query parameter
                from fastapi.responses import RedirectResponse
                redirect_url = f"{frontend_redirect_uri}?access_token={token}&token_type=bearer"
                return RedirectResponse(url=redirect_url)
            else:
                # Fallback: return JSON response
                return {"access_token": token, "token_type": "bearer"}
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    async def register_student(self, request: StudentSchema.StudentCreate):
        try:
            check_email = self.db.query(StudentModel).filter(StudentModel.email == request.email).first()
            secret, otp_uri = generate_2fa_secret(request.email)
            qr_code = generate_qrcode(otp_uri)

            if check_email:
                if check_email.secret_2fa is None:
                    check_email.secret_2fa = secret
                    self.db.commit()
                    self.db.refresh(check_email)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            registered_student = StudentModel(**request.model_dump(), secret_2fa=secret, status_2fa=True)
            self.db.add(registered_student)
            self.db.commit()
            self.db.refresh(registered_student)

            token = create_jwt({
                "email": registered_student.email,
                "name": registered_student.name,
                "role": "Student",
                "from_project": "OAuth2.0 FastAPI"
            })

            std_response = StudentResponse(
                id=registered_student.id,
                name=registered_student.name,
                email=registered_student.email,
                age=registered_student.age,
                IsStudent=registered_student.IsStudent,
                access_token=token,
                qr_code_2fa=qr_code
            )
            return std_response

        except Exception as ex:
            self.db.rollback()
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            )

    async def register_author(self, request: AuthorSchema.CreateAuthor):
        try:
            if not request.email.endswith(f"@{os.getenv('AUTHOR_EMAILS', '')}"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Enter email '{request.email}' not for author registration"
                )

            secret, otp_uri = generate_2fa_secret(request.email)
            qr_code = generate_qrcode(otp_uri)

            verify_email_exists = self.db.query(AuthorModel).filter(AuthorModel.email == request.email).first()
            if verify_email_exists:
                if verify_email_exists.secret_2fa is None:
                    verify_email_exists.secret_2fa = secret
                    self.db.commit()
                    self.db.refresh(verify_email_exists)
                raise HTTPException(
                    status_code=400,
                    detail="Author already registered"
                )

            register_author_model = AuthorModel(**request.model_dump(), secret_2fa=secret, status_2fa=True)
            self.db.add(register_author_model)
            self.db.commit()
            self.db.refresh(register_author_model)

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
                "qr_code": {
                    "qr_code_2fa": qr_code
                }
            })

            return response

        except Exception as ex:
            self.db.rollback()
            code = getattr(500, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )
    # endregion Register

    #region Login
    async def google_login(self, email: str, otp: Optional[str] = None):
        try:
            verify_email = self.db.query(UserModel).filter(UserModel.email == email).first()
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

                code = await self.email_service.email_code()

                subject = "(EmailSent) Test from FastAPI"
                body = await self.email_service.login_template(code, verify_email.name)
                await self.email_service.send_email(
                    verify_email.email,
                    subject, 
                    body
                    )

            elif verify_email.status_2fa is False:
                token = create_jwt({
                    "email": verify_email.email,
                    "name": verify_email.name,
                    "role": verify_email.role,
                    "from_project": "OAuth2.0 FastAPI"
                })

                code = await self.email_service.email_code()

                subject = "(EmailSent) Test from FastAPI"
                body = await self.email_service.login_template(code)
                await self.email_service.send_email(
                    verify_email.email,
                    subject, 
                    body
                    )
                    
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

    async def login(self, email: str, otp: Optional[str] = None):
        try:
            get_email = email.endswith(f"{os.getenv('AUTHOR_EMAILS', '')}")
            if get_email:
                verify_author_email = self.db.query(AuthorModel).filter(AuthorModel.email == email).first()
                if not verify_author_email:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Entered details not found anywhere"
                    )

                if verify_author_email.status_2fa is True:
                    totp = pyotp.TOTP(verify_author_email.secret_2fa)
                    if not totp.verify(otp):
                        raise HTTPException(status_code=400, detail="Invalid OTP code")

                code = await self.email_service.email_code()

                subject = "(EmailSent) Test from FastAPI"
                body = await self.email_service.login_template(code, verify_author_email.name)
                await self.email_service.send_email(
                    verify_author_email.email,
                    subject,
                    body
                )

                new_email = verify_author_email.email
                name = verify_author_email.name
                role = "Author"

            elif not get_email:
                verify_student_email = self.db.query(StudentModel).filter(StudentModel.email == email).first()
                if not verify_student_email:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Entered details not found anywhere"
                    )

                if verify_student_email.status_2fa is True:
                    totp = pyotp.TOTP(verify_student_email.secret_2fa)
                    if not totp.verify(otp):
                        raise HTTPException(status_code=400, detail="Invalid OTP code")

                code = await self.email_service.email_code()

                subject = "(EmailSent) Test from FastAPI"
                body = await self.email_service.login_template(code, verify_student_email.name)
                await self.email_service.send_email(
                    verify_student_email.email,
                    subject,
                    body
                )

                new_email = verify_student_email.email
                name = verify_student_email.name
                role = "Student"

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
    #endregion Login