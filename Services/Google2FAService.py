import os

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from FileLogging.SimpleLogging import simplelogging
from Interfaces.IGoogle2FAService import IGoogle2FAService
from Models.Author import Author as AuthorModel
from Models.Student import Student as StudentModel
from Schema.Google2FASchema import Google2FAResponse
from TwoFAgoogle.SecretandQRCode import generate_2fa_secret, generate_qrcode
from Models.User import User as UserModel

logger = simplelogging("Google2FAService")

class Google2FAService(IGoogle2FAService):
    def __init__(self, db: Session):
        self.db = db

    def enable_2FA(self, email: str):
        try:
            get_email = email.endswith(f"{os.getenv('AUTHOR_EMAILS', '')}")
            if get_email:
                author_details = self.db.query(AuthorModel).filter(AuthorModel.email == email).first()
                if author_details:
                    if author_details.status_2fa is True:
                        logger.info(f"2FA already enabled for the author: {email}")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"2FA already enabled for {email}"
                        )

                secret, otp_uri = generate_2fa_secret(author_details.email)
                qr_code = generate_qrcode(otp_uri)

                logger.info(f"For Author '{email}' successfully generated the 2FA code: {secret}")

                author_details.secret_2fa = secret
                author_details.status_2fa = True
                self.db.commit()
                self.db.refresh(author_details)
                response = Google2FAResponse(
                    msg="ThankYou for enabled 2FA, Scan the qr_code from google authenticator",
                    qr_code_2fa=qr_code)

                logger.info(f"2FA enabled successfully for the author: {email}")

                return response
            elif not get_email:
                student_details = self.db.query(StudentModel).filter(StudentModel.email == email).first()
                if student_details:
                    if student_details.status_2fa is True:
                        logger.info(f"2FA already enabled for the student: {email}")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"2FA already enabled for {email}"
                        )
                secret, otp_uri = generate_2fa_secret(student_details.email)
                qr_code = generate_qrcode(otp_uri)

                logger.info(f"For Student '{email}' successfully generated the 2FA code: {secret}")

                student_details.secret_2fa = secret
                student_details.status_2fa = True
                self.db.commit()
                self.db.refresh(student_details)
                response = Google2FAResponse(
                    msg="ThankYou for enabled 2FA, Scan the qr_code from google authenticator",
                    qr_code_2fa=qr_code
                )

                logger.info(f"2FA enabled successfully for the student: {email}")

                return response
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Entered details not found anywhere"
                )
        except Exception as ex:
            code = getattr(ex, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def google_enable_2fa(self, email: str):
        try:
            get_email = self.db.query(UserModel).filter(UserModel.email == email).first()
            if get_email:
                if get_email.status_2fa:

                    logger.info(f"2FA already enabled for the google user: {email}")

                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"2FA already enabled for {email}"
                    )
                secret, otp_uri = generate_2fa_secret(get_email.email)
                qr_code = generate_qrcode(otp_uri)

                logger.info(f"For google user '{email}' successfully generated the 2FA code: {secret}")

                get_email.secret_2fa = secret
                get_email.status_2fa = True
                self.db.commit()
                self.db.refresh(get_email)
                response = Google2FAResponse(
                    msg="ThankYou for enabled 2FA, Scan the qr_code from google authenticator",
                    qr_code_2fa=qr_code
                )

                logger.info(f"2FA enabled successfully for the google user: {email}")

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

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def google_disable_2fa(self, email: str):
        try:
            get_email = self.db.query(UserModel).filter(UserModel.email == email).first()
            if get_email:
                if get_email.status_2fa:
                    get_email.status_2fa = False
                    get_email.secret_2fa = None
                    self.db.commit()
                    self.db.refresh(get_email)

                    logger.info(f"2FA disabled successfully for the google user: {email}")

                    return {"msg": "2FA disabled successfully"}
                else:

                    logger.info(f"2FA already disabled for the google user: {email}")

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

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def disable_2fa(self, email: str):
        try:
            get_email = email.endswith(f"{os.getenv('AUTHOR_EMAILS', '')}")
            if get_email:
                author_details = self.db.query(AuthorModel).filter(AuthorModel.email == email).first()
                if author_details:
                    if author_details.secret_2fa:
                        author_details.secret_2fa = None
                        author_details.status_2fa = False
                        self.db.commit()
                        self.db.refresh(author_details)

                        logger.info(f"2FA disabled successfully for the author: {email}")

                        return {"msg": "2FA disabled successfully"}

                    logger.info(f"2FA already disabled for the author: {email}")

                    return {"msg": "2FA already disabled"}
            elif not get_email:
                student_details = self.db.query(StudentModel).filter(StudentModel.email == email).first()
                if student_details:
                    if student_details.secret_2fa:
                        student_details.secret_2fa = None
                        student_details.status_2fa = False
                        self.db.commit()
                        self.db.refresh(student_details)
                        logger.info(f"2FA disabled successfully for the student: {email}")

                        return {"msg": "2FA disabled successfully"}

                    logger.info(f"2FA already disabled for the student: {email}")

                    return {"msg": "2FA already disabled"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Entered details not found anywhere"
                )
        except Exception as ex:
            code = getattr(ex, 'status_code', status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )