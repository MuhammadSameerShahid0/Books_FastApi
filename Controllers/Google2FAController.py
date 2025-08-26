from fastapi import FastAPI, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from Database import get_db
from Interfaces.IGoogle2FAService import IGoogle2FAService
from Schema.Google2FASchema import Google2FAResponse
from Services.Google2FAService import Google2FAService

app = FastAPI()
Google2FA = APIRouter(tags=["Google2FA"])

def get_google2FA_service(db: Session = Depends(get_db)) -> IGoogle2FAService:
    return Google2FAService(db)

Google2FA_DB_DI = Depends(get_google2FA_service)

@Google2FA.post("/enable-2FA", response_model=Google2FAResponse)
def enable_2fa(email: str, service : IGoogle2FAService = Google2FA_DB_DI):
    return service.enable_2FA(email)

@Google2FA.post("/google-enable-2FA", response_model=Google2FAResponse)
def google_enable_2fa(email: str, service : IGoogle2FAService = Google2FA_DB_DI):
    return service.google_enable_2fa(email)

@Google2FA.post("/google-disable-2FA")
def google_disable_2fa(email: str, service : IGoogle2FAService = Google2FA_DB_DI):
    return service.google_disable_2fa(email)

@Google2FA.post("/disable-2FA")
def disable_2fa(email: str, service : IGoogle2FAService = Google2FA_DB_DI):
    return service.disable_2fa(email)