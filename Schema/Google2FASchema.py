from pydantic import BaseModel


class Google2FAResponse(BaseModel):
    msg : str
    qr_code_2fa: str