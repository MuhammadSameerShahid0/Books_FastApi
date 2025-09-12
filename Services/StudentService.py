from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from FileLogging.SimpleLogging import simplelogging
from Interfaces.IStudentService import IStudentService
from Models.Student import Student as StudentModel
from Schema import StudentSchema

logger = simplelogging("StudentService")

class StudentService(IStudentService):
    def __init__(self, db: Session):
        self.db = db

    def student_list(self):
        try:
            db_student = self.db.query(StudentModel).all()
            logger.info("'Admin' request to get the list of students")
            return db_student
        except Exception as ex:
            logger.error(f"Something went wrong, error details is {ex}")
            return {"Error": str(ex)}

    def student_by_id(self, student_id: int):
        try:
            std_model = StudentModel
            std_id = self.db.query(std_model).filter(std_model.id == student_id).first()
            if not std_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student not found"
                )
            else:
                logger.info(f"Request Successful, to get the students details by id {student_id}")
                return std_id
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")
            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def student_is_true(self):
        try:
            is_std_true = self.db.query(StudentModel).filter(StudentModel.IsStudent == "True").all()
            logger.info("'Admin' request to get the list of true students")
            return is_std_true
        except Exception as ex:
            logger.error(f"Something went wrong, error details is {ex}")
            return {"error": str(ex)}

    def update_Student(self,student_id: int,
            email: str,
            request: StudentSchema.StudentUpdate, ):
        try:
            student = self.db.query(StudentModel).filter(StudentModel.id == student_id, StudentModel.IsStudent == "True").first()
            if student:
                if student.email != email:
                    logger.error(f"Entered email {email} does not match with student {student.email}")
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

                email_check = self.db.query(StudentModel).filter(StudentModel.email == request.email).first()
                if not email_check:
                    update_data = request.model_dump(exclude_unset=True)
                    for field, value in update_data.items():
                          setattr(student, field, value)

                    self.db.commit()
                    self.db.refresh(student)

                    logger.info(f"Student '{student.name}' details updated for email {student.email}")

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

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def delete_Student(self,request: StudentSchema.StudentDelete):
        try:
            errors = []
            std_id_db =  self.db.query(StudentModel).filter(
                StudentModel.id == request.id
            ).first()

            if std_id_db is not None:
                if std_id_db.email != request.email:
                    errors.append(f"Email : '{request.email}' not correct against id : {request.id}")

            verify_record = self.db.query(StudentModel).filter(StudentModel.email == request.email).first()
            if verify_record is not None:
                if std_id_db is None:
                    errors.append(f"Id not found against this email")
                elif std_id_db.id != verify_record.id:
                    errors.append(f"Id not correct against email : '{request.email}'")

            if std_id_db is None and verify_record is None:
                errors.append(f"Student Id '{request.id}' and email '{request.email}' not correct")

            errors_len = len(errors)
            if errors_len > 0:
                logger.error(f"Admin try to delete the student but got the additional errors: {errors}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str.join(" ! ", errors)
                )

            self.db.delete(std_id_db)
            self.db.commit()
            logger.info(f"Admin deleted the student {request.email}")

            return f'Student deleted successfully. Id : {verify_record.id} name : {verify_record.name}'

        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )
