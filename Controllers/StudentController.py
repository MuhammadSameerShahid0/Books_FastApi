from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
import Models.Student as StudentModel
from Database import get_db
from Interfaces.IStudentService import IStudentService
from OAuthandJwt.JWTToken import require_role
from Schema import StudentSchema
from Schema.StudentSchema import UpdateStudentResponse
from Services.StudentService import StudentService

app = FastAPI()
Student = APIRouter(tags=["Student"])

def get_student_service(db: Session = Depends(get_db)) -> IStudentService:
    return StudentService(db)

Student_DB_DI = Depends(get_student_service)

class StudentController:
    @Student.get("/student_list")
    def get_student_list(service : IStudentService = Student_DB_DI,
                         current_user: dict = Depends(require_role(["Admin"]))):
        return service.student_list()

    @Student.get("/student_by_id")
    def get_student_by_id(student_id: int, service : IStudentService = Student_DB_DI, current_user: dict = Depends(require_role(["Admin" , "Student"]))):
        return service.student_by_id(student_id)

    @Student.get("/IsStudent_True")
    def get_student_is_true(student_id: int, service : IStudentService = Student_DB_DI, current_user: dict = Depends(require_role(["Admin"]))):
        return service.student_is_true(student_id)

    @Student.post("/Update_Student_If_IsStudent_True",
                  response_model=UpdateStudentResponse,)
    async def update_student(
            student_id: int,
            email: str,
            request: StudentSchema.StudentUpdate,
            service : IStudentService = Student_DB_DI,
            current_user: dict = Depends(require_role(["Admin", "Student"]))
    ):
        return service.update_Student(student_id, email, request)


    @Student.delete("/Delete_Student_By_id")
    def delete_student_by_id(request: StudentSchema.StudentDelete,
                                   service : IStudentService = Student_DB_DI,
                                   current_user: dict = Depends(require_role(["Admin"]))):
        return service.delete_Student(request)