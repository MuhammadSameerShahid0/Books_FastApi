from datetime import datetime
from typing import Optional

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from Models import StudentBook
from Models.Books import Book as BookModel
from Models.Student import Student as StudentModel
from Database import get_db
from Schema import BookSchema
from Schema.BookSchema import ResponseAssignBookToStudent
from Schema.studentbookenum import Status

app = FastAPI()
Books = APIRouter(tags=["Books"])


class BooksController:
    @Books.post("/create_book")
    async def create_book(request: BookSchema.CreateBook, db: Session = Depends(get_db)):
        try:
            check_title = db.query(BookModel).filter(
                BookModel.title == request.title
            ).first()

            if check_title is None:
                create_book = BookModel(**request.model_dump())

                db.add(create_book)
                db.commit()
                db.refresh(create_book)
                return create_book
            else:
                raise HTTPException(status_code=400, detail="Book already exists")

        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    @Books.post("/assign_book_to_student")
    def assign_book_to_student(request: BookSchema.AssignBookToStudent, db: Session = Depends(get_db)):
        try:
            book_exists = db.query(BookModel).filter(
                BookModel.id == request.book_id, BookModel.title == request.book_title
            ).first()

            if book_exists:
                student_exists = db.query(StudentModel).filter(
                    StudentModel.id == request.student_id, StudentModel.email == request.student_email
                ).first()
                if student_exists:
                    student_book_exists = db.query(StudentBook).filter(
                        StudentBook.book_id == book_exists.id,
                        StudentBook.student_id == student_exists.id,
                        StudentBook.Status != str(Status.Return_Successfully)
                    ).first()

                    if student_book_exists:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Book already assigned to student '{student_exists.name}'"
                        )

                    student_book = StudentBook(student_id=student_exists.id, book_id=book_exists.id)

                    student_book.AssignedAt = datetime.now().today()
                    student_book.ReturnDate = None
                    student_book.Status = str(Status.Pending_for_Return)

                    db.add(student_book)
                    db.commit()
                    db.refresh(student_book)

                    return ResponseAssignBookToStudent(
                        Student_Name=student_exists.name,
                        Student_Email=student_exists.email,
                        Book_Title=book_exists.title,
                        Book_Author=book_exists.author,
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

    @Books.post("/return_book_from_student")
    def return_book(request: BookSchema.ReturnBook, db: Session = Depends(get_db)):
        try:
            get_book_id = db.query(BookModel).filter(BookModel.title == request.book_title).first()
            get_std_id = db.query(StudentModel).filter(StudentModel.email == request.student_email).first()

            if get_book_id is None or get_std_id is None:
                raise HTTPException(status_code=404, detail="Enter details not found")

            Student_Book = db.query(StudentBook).filter(
                StudentBook.student_id == get_std_id.id,
                StudentBook.book_id == get_book_id.id,
                StudentBook.Status != str(Status.Return_Successfully)
            ).first()

            if Student_Book:
                Student_Book.Status = str(Status.Return_Successfully)
                Student_Book.ReturnDate = datetime.now().today()
                db.commit()
                db.refresh(Student_Book)
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

    @Books.get("/pending_or_return_book")
    def pending_books(PendingBooks: Optional[str] = None,
                      ReturnBooks: Optional[str] = None,
                      db: Session = Depends(get_db)):
        try:
            if PendingBooks is not None and ReturnBooks is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Use only 1 option"
                )

            if PendingBooks is not None:
                get_pending_books = db.query(StudentBook).filter(
                    StudentBook.Status == str(Status.Pending_for_Return)).all()
                if get_pending_books:
                    result = []
                    for pending_book in get_pending_books:
                        std_details = db.query(StudentModel).filter(StudentModel.id == pending_book.student_id).first()
                        book_details = db.query(BookModel).filter(BookModel.id == pending_book.book_id).first()

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
                get_returning_books = db.query(StudentBook).filter(
                    StudentBook.Status == str(Status.Return_Successfully)).all()
                if get_returning_books:
                    result = []
                    for return_book in get_returning_books:
                        std_details = db.query(StudentModel).filter(StudentModel.id == return_book.student_id).first()
                        book_details = db.query(BookModel).filter(BookModel.id == return_book.book_id).first()

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
