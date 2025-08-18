import os

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from Models.User import User as UserModel
from Models.Author import  Author as AuthorModel
from Models.Student import Student as StudentModel
from Database import get_db
from Schema.Google2FASchema import Google2FAResponse
from TwoFAgoogle.SecretandQRCode import generate_2fa_secret, generate_qrcode

app = FastAPI()
Google2FA = APIRouter(tags=["Google2FA"])

@Google2FA.post("/enable-2FA", response_model=Google2FAResponse)
def enable_2fa(email: str, db: Session = Depends(get_db)):
    try:
        get_email = email.endswith(f"{os.getenv('AUTHOR_EMAILS', '')}")
        if get_email:
            author_details = db.query(AuthorModel).filter(AuthorModel.email == email).first()
            if author_details:
                if author_details.status_2fa is True:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"2FA already enabled for {email}"
                    )

            secret, otp_uri = generate_2fa_secret(author_details.email)
            qr_code = generate_qrcode(otp_uri)
            author_details.secret_2fa = secret
            author_details.status_2fa = True
            db.commit()
            db.refresh(author_details)
            response = Google2FAResponse(
                msg="ThankYou for enabled 2FA, Scan the qr_code from google authenticator",
                qr_code_2fa=qr_code)
            return response
        elif not get_email:
            student_details = db.query(StudentModel).filter(StudentModel.email == email).first()
            if student_details:
                if student_details.status_2fa is True:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"2FA already enabled for {email}"
                    )
            secret, otp_uri = generate_2fa_secret(student_details.email)
            qr_code = generate_qrcode(otp_uri)
            student_details.secret_2fa = secret
            student_details.status_2fa = True
            db.commit()
            db.refresh(student_details)
            response = Google2FAResponse(
                msg="ThankYou for enabled 2FA, Scan the qr_code from google authenticator",
                qr_code_2fa=qr_code
            )
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entered details not found anywhere"
            )
    except Exception as  ex:
        code = getattr(ex, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )

@Google2FA.post("/google-enable-2FA", response_model=Google2FAResponse)
def google_enable_2fa(email: str, db: Session = Depends(get_db)):
    try:
        get_email = db.query(UserModel).filter(UserModel.email == email).first()
        if get_email:
            if get_email.status_2fa:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"2FA already enabled for {email}"
                )
            secret, otp_uri = generate_2fa_secret(get_email.email)
            qr_code = generate_qrcode(otp_uri)
            get_email.secret_2fa = secret
            get_email.status_2fa = True
            db.commit()
            db.refresh(get_email)
            response = Google2FAResponse(
                msg="ThankYou for enabled 2FA, Scan the qr_code from google authenticator",
                qr_code_2fa=qr_code
            )
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entered details not found anywhere"
            )
    except Exception as ex:
        code = getattr(ex, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )

@Google2FA.post("/google-disable-2FA")
def google_disable_2fa(email: str, db: Session = Depends(get_db)):
    try:
        get_email = db.query(UserModel).filter(UserModel.email == email).first()
        if get_email:
            if get_email.status_2fa:
                get_email.status_2fa = False
                get_email.secret_2fa = None
                db.commit()
                db.refresh(get_email)
                return {"msg": "2FA disabled successfully"}
            else:
                return {"msg": "2FA already disabled"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entered details not found anywhere"
            )
    except Exception as ex:
        code = getattr(ex, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex

        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )

@Google2FA.post("/disable-2FA")
def disable_2fa(email: str, db: Session = Depends(get_db)):
    try:
        get_email = email.endswith(f"{os.getenv('AUTHOR_EMAILS', '')}")
        if get_email:
            author_details = db.query(AuthorModel).filter(AuthorModel.email == email).first()
            if author_details:
                if author_details.secret_2fa:
                    author_details.secret_2fa = None
                    author_details.status_2fa = False
                    db.commit()
                    db.refresh(author_details)
                    return {"msg": "2FA disabled successfully"}
                return {"msg": "2FA already disabled"}
        elif not get_email:
            student_details = db.query(StudentModel).filter(StudentModel.email == email).first()
            if student_details:
                if student_details.secret_2fa:
                    student_details.secret_2fa = None
                    student_details.status_2fa = False
                    db.commit()
                    db.refresh(student_details)
                    return {"msg": "2FA disabled successfully"}
                return {"msg": "2FA already disabled"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entered details not found anywhere"
            )
    except Exception as  ex:
        code = getattr(ex, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(ex, HTTPException):
            raise ex
        raise HTTPException(
            status_code=code,
            detail=str(ex)
        )

