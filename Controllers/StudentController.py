from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
import Models.Student as StudentModel
from Database import get_db
from OAuthandJwt.JWTToken import require_role
from Schema import StudentSchema
from Schema.StudentSchema import UpdateStudentResponse

app = FastAPI()
Student = APIRouter(tags=["Student"])


class StudentController:

    @Student.get("/student_list")
    def get_student_list(db: Session = Depends(get_db), current_user: dict = Depends(require_role(["Admin"]))):
        try:
            db_student = db.query(StudentModel).all()
            return db_student
        except Exception as ex:
            return {"Error": str(ex)}

    @Student.get("/student_by_id")
    def get_student_by_id(student_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_role(["Admin" , "Student"]))):
        try:
            std_model = StudentModel
            std_id = db.query(std_model).filter(std_model.id == student_id).first()
            if not std_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student not found"
                )
            else:
                return std_id
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    @Student.get("/IsStudent_True")
    def get_student_is_true(db: Session = Depends(get_db),current_user: dict = Depends(require_role(["Admin"]))):
        try:
            is_std_true = db.query(StudentModel).filter(StudentModel.IsStudent == "True").all()
            return is_std_true
        except Exception as ex:
            return {"error": str(ex)}

    @Student.post("/Update_Student_If_IsStudent_True",
                  response_model=UpdateStudentResponse,)
    async def update_student(
            student_id: int,
            email: str,
            request: StudentSchema.StudentUpdate,
            db: Session = Depends(get_db),
            current_user: dict = Depends(require_role(["Admin", "Student"]))
    ):
        try:
            student = db.query(StudentModel).filter(StudentModel.id == student_id, StudentModel.IsStudent == "True").first()
            if student:
                if student.email != email:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Entered email does not match"
                    )

                if not request.email:
                    request.email = student.email
                if not request.name:
                    request.name = student.name
                if not request.age:
                    request.age = student.age

                email_check = db.query(StudentModel).filter(StudentModel.email == request.email).first()
                if not email_check:
                    update_data = request.model_dump(exclude_unset=True)
                    for field, value in update_data.items():
                          setattr(student, field, value)

                    db.commit()
                    db.refresh(student)
                    return student
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already registered"
                        )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student not active"
                )
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    @Student.delete("/Delete_Student_By_id")
    def delete_student_by_id(request: StudentSchema.StudentDelete,
                                   db: Session = Depends(get_db),
                                   current_user: dict = Depends(require_role(["Admin"]))):
        try:
            errors = []
            std_id_db =  db.query(StudentModel).filter(
                StudentModel.id == request.id
            ).first()

            if std_id_db is not None:
                if std_id_db.email != request.email:
                    errors.append(f"Email : '{request.email}' not correct against id : {request.id}")

            verify_record = db.query(StudentModel).filter(StudentModel.email == request.email).first()
            if verify_record is not None:
                if std_id_db is None:
                    errors.append(f"Id not found against this email")
                elif std_id_db.id != verify_record.id:
                    errors.append(f"Id not correct against email : '{request.email}'")

            if std_id_db is None and verify_record is None:
                errors.append(f"Student Id '{request.id}' and email '{request.email}' not correct")

            errors_len = len(errors)
            if errors_len > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str.join(" ! ", errors)
                )

            db.delete(std_id_db)
            db.commit()
            return f'Student deleted successfully. Id : {verify_record.id} name : {verify_record.name}'

        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )
