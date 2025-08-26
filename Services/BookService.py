from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from Interfaces.IBookService import IBookService
from Models.Author import Author as AuthorModel
from Models.Books import Book as BookModel
from Schema import BookSchema
from Schema.BookSchema import ResponseAssignBookToStudent
from Models.Student import Student as StudentModel
from Models.StudentBook import StudentBook as StudentBookModel
from Schema.studentbookenum import Status


class BookService(IBookService):
    def __init__(self, db: Session):
        self.db = db

    async def create_book(self, request: BookSchema.CreateBook):
        try:
            check_title = self.db.query(BookModel).filter(
                BookModel.title == request.title
            ).first()

            if check_title is None:
                verify_author_id = self.db.query(AuthorModel).filter(
                    AuthorModel.id == request.author_id
                ).first()
                if verify_author_id:
                    create_book_response = BookModel(**request.model_dump())

                    self.db.add(create_book_response)
                    self.db.commit()
                    self.db.refresh(create_book_response)
                    return create_book_response
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Author not found")
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Book already exists")

        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def assign_book_to_student(self, request: BookSchema.AssignBookToStudent):
        try:
            book_exists = self.db.query(BookModel).filter(
                BookModel.id == request.book_id, BookModel.title == request.book_title
            ).first()

            if book_exists:
                student_exists = self.db.query(StudentModel).filter(
                    StudentModel.id == request.student_id, StudentModel.email == request.student_email
                ).first()
                if student_exists:
                    student_book_exists = self.db.query(StudentBookModel).filter(
                        StudentBookModel.book_id == book_exists.id,
                        StudentBookModel.student_id == student_exists.id,
                        StudentBookModel.Status != str(Status.Return_Successfully)
                    ).first()

                    if student_book_exists:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Book already assigned to student '{student_exists.name}'"
                        )

                    student_book = StudentBookModel(student_id=student_exists.id, book_id=book_exists.id)

                    student_book.AssignedAt = datetime.now().today()
                    student_book.ReturnDate = None
                    student_book.Status = str(Status.Pending_for_Return)

                    self.db.add(student_book)
                    self.db.commit()
                    self.db.refresh(student_book)

                    return ResponseAssignBookToStudent(
                        Student_Name=student_exists.name,
                        Student_Email=student_exists.email,
                        Book_Title=book_exists.title,
                        Book_Author=book_exists.author.name,
                        AssignedAt=datetime.now()
                    )
                else:
                    raise HTTPException(status_code=404, detail="Student not found")

            else:
                raise HTTPException(status_code=404, detail="Book not found")

        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex
            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def return_book_from_student(self,request: BookSchema.ReturnBook):
        try:
            get_book_id = self.db.query(BookModel).filter(BookModel.title == request.book_title).first()
            get_std_id = self.db.query(StudentModel).filter(StudentModel.email == request.student_email).first()

            if get_book_id is None or get_std_id is None:
                raise HTTPException(status_code=404, detail="Enter details not found")

            Student_Book = self.db.query(StudentBookModel).filter(
                StudentBookModel.student_id == get_std_id.id,
                StudentBookModel.book_id == get_book_id.id,
                StudentBookModel.Status == str(Status.Pending_for_Return)
            ).first()

            if Student_Book:
                Student_Book.Status = str(Status.Return_Successfully)
                Student_Book.ReturnDate = datetime.now().today()
                self.db.commit()
                self.db.refresh(Student_Book)
                return f"ThankYou '{get_std_id.name}' for using book '{request.book_title}'"
            else:
                raise HTTPException(status_code=404, detail="Book already returned or details not found")
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex
            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def pending_or_return_book(self,
                               PendingBooks: Optional[str] = None,
                               ReturnBooks: Optional[str] = None ):
        try:
            if PendingBooks is not None and ReturnBooks is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Use only 1 option"
                )

            if PendingBooks is not None:
                get_pending_books = self.db.query(StudentBookModel).filter(
                    StudentBookModel.Status == str(Status.Pending_for_Return)).all()
                if get_pending_books:
                    result = []
                    for pending_book in get_pending_books:
                        std_details = self.db.query(StudentModel).filter(StudentModel.id == pending_book.student_id).first()
                        book_details = self.db.query(BookModel).filter(BookModel.id == pending_book.book_id).first()

                        pending_book_data = {
                            **pending_book.__dict__,
                            "Student_name": std_details.name,
                            "Book_title": book_details.title,
                        }
                        result.append(pending_book_data)

                    return result
                else:
                    raise HTTPException(status_code=404, detail="Pending Book record not found")

            elif ReturnBooks is not None:
                get_returning_books = self.db.query(StudentBookModel).filter(
                    StudentBookModel.Status == str(Status.Return_Successfully)).all()
                if get_returning_books:
                    result = []
                    for return_book in get_returning_books:
                        std_details = self.db.query(StudentModel).filter(StudentModel.id == return_book.student_id).first()
                        book_details = self.db.query(BookModel).filter(BookModel.id == return_book.book_id).first()

                        return_book_data = {
                            **return_book.__dict__,
                            "Student_name": std_details.name,
                            "Book_title": book_details.title,
                        }
                        result.append(return_book_data)

                    return result
                else:
                    raise HTTPException(status_code=404, detail="Returning Book record not found")
            else:
                raise HTTPException(status_code=404, detail="Kindly fill at least 1 option")

        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex
            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def record_by_author_id(self, author_id: int):
        try:
            get_author_record = self.db.query(BookModel).filter(
                BookModel.author_id == author_id,
            ).all()

            if len(get_author_record) is not 0:
                result = []
                for record in get_author_record:
                    author_details = self.db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
                    return_record = {
                    **record.__dict__,
                    "Author Name": author_details.name,
                    "Author Nationality": author_details.nationality,
                    }

                    result.append(return_record)
                return result
            else:
                raise HTTPException(status_code=404, detail="Author not found")
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

