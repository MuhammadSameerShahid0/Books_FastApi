from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session

from Database import get_db
from Factory.factories import ServiceFactory
from Interfaces.IStudentProfileService import IStudentProfileService
from OAuthandJwt.JWTToken import require_role
from Schema.StudentProfileSchema import UpdateProfile
from Services.StudentProfileService import StudentProfileService

app = FastAPI()
StudentProfiles = APIRouter(tags=["StudentProfile"])

def get_studentprofile_service(db: Session = Depends(get_db)) -> IStudentProfileService:
    return ServiceFactory.get_services("studentprofile", db)

StudentProfile_DB_DI = Depends(get_studentprofile_service)

class StudentProfileController:

    @StudentProfiles.post("/update_Student_profile")
    def update_student_profile(request: UpdateProfile, service: IStudentProfileService = StudentProfile_DB_DI,
                               current_user: dict = Depends(require_role(["Admin" , "Student"]))):
        return service.update_student_profile(request)

    @StudentProfiles.get("/list_of_Student_profiles")
    def get_list_of_student_profiles(service: IStudentProfileService = StudentProfile_DB_DI,
                                     current_user: dict = Depends(require_role(["Admin"]))):
        return service.list_of_student_profile()

    @StudentProfiles.get("/student_id")
    def get_student_id(student_id: int, service: IStudentProfileService = StudentProfile_DB_DI,
                       current_user: dict = Depends(require_role(["Admin", "Student"]))):
        return service.student_by_id(student_id)
