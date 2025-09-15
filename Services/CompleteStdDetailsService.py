from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette import status

from FileLogging.SimpleLogging import simplelogging
from Interfaces.ICompleteStdDetailsService import ICompleteStdDetailsService
from Models.StudentBook import StudentBook as StudentBookModel
from Models.Books import Book as BookModel
from Models.Student import Student as StudentModel
from Schema.StdDetailsSchema import StdDetailsSchema

logger = simplelogging("CompleteStdDetailsService")

class CompleteStdDetailsService(ICompleteStdDetailsService):
    def __init__(self, db: Session):
        self.db = db

    def std_details(self, student_id: int):
        try:
            get_details = (
                self.db.query(StudentBookModel)
                .options(joinedload(StudentBookModel.student)
                         .joinedload(StudentModel.student_profile)
                         )
                .options(joinedload(StudentBookModel.book)
                         .joinedload(BookModel.author)
                         )
                .filter(StudentBookModel.student_id == student_id)
                .all()
            )
            result = []
            if get_details:
                logger.info(f"Student details found for id {student_id}")
                for detail in get_details:
                    result_data = StdDetailsSchema(
                        Name=detail.student.name if detail.student else None,
                        Email=detail.student.email if detail.student else None,
                        Age=detail.student.age if detail.student else None,
                        Address=detail.student.student_profile.address if detail.student.student_profile else None,
                        Phone_Number=detail.student.student_profile.phone_number if detail.student.student_profile else None,
                        Date_of_Birth=detail.student.student_profile.dob if detail.student.student_profile else None,
                        Book_Title=detail.book.title if detail.book else None,
                        Book_Description=detail.book.description if detail.book else None,
                        Book_Year=detail.book.year if detail.book else None,
                        Book_AssignedAt=detail.AssignedAt if detail.AssignedAt else None,
                        Book_ReturnDate=detail.ReturnDate if detail.ReturnDate else None,
                        Status=detail.Status if detail.Status else None,
                        Author_Name=detail.book.author.name if detail.book.author else None,
                        Author_Bio=detail.book.author.bio if detail.book.author else None,
                        Author_Nationality=detail.book.author.nationality if detail.book.author else None
                    )
                    result.append(result_data)

                    logger.info(f"Successfully get complete student details for student {detail.student.name}")

                return result
            else:
                raise HTTPException(status_code=404, detail="Student not found")
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def pending_or_return(self, student_id: int,
                          pending: Optional[str] = None,
                          Return: Optional[str] = None,):
        try:
            if not (pending or Return) or (pending and Return):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Use exactly one option (pending or Return)"
                )

            status_filter = "Pending for Return" if pending else "Return Successfully"
            get_details = (
                self.db.query(StudentBookModel)
                .options(joinedload(StudentBookModel.student)
                         .joinedload(StudentModel.student_profile)
                         )
                .options(joinedload(StudentBookModel.book)
                         .joinedload(BookModel.author)
                         )
                .filter(StudentBookModel.student_id == student_id, StudentBookModel.Status == status_filter)
                .all()
            )

            action = "assigned to" if pending else "returned from"
            if not get_details:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No book {action} this student"
                )

            result = []
            for detail in get_details:
                result_data = StdDetailsSchema(
                    Name=detail.student.name if detail.student else None,
                    Email=detail.student.email if detail.student else None,
                    Age=detail.student.age if detail.student else None,
                    Address=detail.student.student_profile.address if detail.student.student_profile else None,
                    Phone_Number=detail.student.student_profile.phone_number if detail.student.student_profile else None,
                    Date_of_Birth=detail.student.student_profile.dob if detail.student.student_profile else None,
                    Book_Title=detail.book.title if detail.book else None,
                    Book_Description=detail.book.description if detail.book else None,
                    Book_Year=detail.book.year if detail.book else None,
                    Book_AssignedAt=detail.AssignedAt if detail.AssignedAt else None,
                    Book_ReturnDate=detail.ReturnDate if detail.ReturnDate else None,
                    Status=detail.Status if detail.Status else None,
                    Author_Name=detail.book.author.name if detail.book.author else None,
                    Author_Bio=detail.book.author.bio if detail.book.author else None,
                    Author_Nationality=detail.book.author.nationality if detail.book.author else None
                )
                result.append(result_data)

                logger.info(f"Successfully get the detail of {status_filter} student {student_id}")

            return result

        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )
