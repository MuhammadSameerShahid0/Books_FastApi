from typing import Optional
from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session

from Database import get_db
from Interfaces.ICompleteStdDetailsService import ICompleteStdDetailsService
from OAuthandJwt.JWTToken import require_role
from Services.CompleteStdDetailsService import CompleteStdDetailsService

app = FastAPI()
CompleteStdDetails = APIRouter(tags=["CompleteStdDetails"])

def get_CompleteStdDetails_service(db: Session = Depends(get_db)) -> ICompleteStdDetailsService:
    return CompleteStdDetailsService(db)

CompleteStdDetails_DB_DI = Depends(get_CompleteStdDetails_service)

class CompleteStdDetailsController:
    @CompleteStdDetails.get("/Std_Details")
    def std_details(student_id: int, service: ICompleteStdDetailsService = CompleteStdDetails_DB_DI,
                    current_user: dict = Depends(require_role(["Admin" , "Student"]))):
        return service.std_details(student_id)

    @CompleteStdDetails.get("/PendingOrReturnBooks")
    def pending_or_return(student_id: int,
                          pending: Optional[str] = None,
                          Return: Optional[str] = None,
                          service: ICompleteStdDetailsService = CompleteStdDetails_DB_DI,
                          current_user: dict = Depends(require_role(["Admin" , "Student"]))):
        return service.pending_or_return(student_id, pending, Return)