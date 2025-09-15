from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from FileLogging.SimpleLogging import simplelogging
from Interfaces.IStudentProfileService import IStudentProfileService
from Models.StudentProfile import StudentProfile as StudentProfileModel
from Models.Student import Student as StudentModel
from Schema.StudentProfileSchema import UpdateProfile

logger = simplelogging("StudentProfileService")

class StudentProfileService(IStudentProfileService):
    def __init__(self, db : Session):
        self.db = db

    def update_student_profile(self, request: UpdateProfile):
        try:
            verify_student_id = self.db.query(StudentModel).filter(StudentModel.id == request.student_id).first()
            if verify_student_id is None:
                raise HTTPException(status_code=400, detail="Student not found")

            get_studentprofile = self.db.query(StudentProfileModel).filter(StudentProfileModel.student_id == request.student_id).first()
            result = []
            if get_studentprofile is None:
                update_data = StudentProfileModel(**request.model_dump())
                self.db.add(update_data)
                self.db.commit()
                self.db.refresh(update_data)

                result_data = {
                    "Student_name": verify_student_id.name,
                    "Student_email": verify_student_id.email,
                    **get_studentprofile.__dict__
                }
                result.append(result_data)
                return result

            elif get_studentprofile is not None:
                update_data = request.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(get_studentprofile, field, value)
                self.db.commit()
                self.db.refresh(get_studentprofile)

                result_data={
                    "Student_name": verify_student_id.name,
                    "Student_email": verify_student_id.email,
                    **get_studentprofile.__dict__
                }
                result.append(result_data)
                return result
            else:
                raise HTTPException(status_code= 500, detail="Something went wrong")
        except Exception as ex:
            self.db.rollback()
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def list_of_student_profile(self):
        try:
            list_std_profile = self.db.query(StudentProfileModel).all()
            result = []
            if list_std_profile is None:
                raise HTTPException(status_code=404, detail="Student Profile record not found")
            for std_profile in list_std_profile:
                std_details = self.db.query(StudentModel).filter(StudentModel.id == std_profile.student_id).first()

                result_data={
                    "Student Name": std_details.name if std_details is not None else None,
                    "Student Email": std_details.email if std_details is not None else None,
                    "Student Age": std_details.age if std_details is not None else None,
                    **std_profile.__dict__
                }

                result.append(result_data)
            return result
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise  ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def student_by_id(self, student_id: int):
        try:
            result = []
            std_profile_id = self.db.query(StudentProfileModel).filter(StudentProfileModel.student_id == student_id).first()
            if std_profile_id is None:
                raise HTTPException(status_code=404, detail="Student not found")

            std_id= self.db.query(StudentModel).filter(StudentModel.id == std_profile_id.student_id).first()
            if std_id:
                result_data = {
                    **std_profile_id.__dict__,
                    **std_id.__dict__
                }
                result.append(result_data)
                return result
            else:
                raise HTTPException(status_code=404, detail="Student not found")
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex
            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

        # ------Joins------
        # test = (
        #     db.query(StudentModel)
        #     .options(joinedload(StudentModel.student_profile))  # Eager-load the profile
        #     .filter(StudentModel.id == student_id)
        #     .first()
        # )
        # if test:
        #     return test
        # else:
        #     raise HTTPException(status_code=404, detail="Student not found")
