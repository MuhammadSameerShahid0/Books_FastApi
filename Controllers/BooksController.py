from typing import Optional
from fastapi import FastAPI, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from Database import get_db
from Interfaces.IBookService import IBookService
from OAuthandJwt.JWTToken import require_role
from Schema import BookSchema
from Services.BookService import BookService

app = FastAPI()
Books = APIRouter(tags=["Books"])

def get_book_service(db: Session = Depends(get_db)) -> IBookService:
    return BookService(db)

Book_Db_DI = Depends(get_book_service)

class BooksController:
    @Books.post("/create_book")
    async def create_book(request: BookSchema.CreateBook, service: IBookService = Book_Db_DI,
                          current_user: dict = Depends(require_role(["Admin"]))):
        return await service.create_book(request)

    @Books.post("/assign_book_to_student")
    def assign_book_to_student(request: BookSchema.AssignBookToStudent,
                               service: IBookService = Book_Db_DI,
                               current_user: dict = Depends(require_role(["Admin"]))):
        return service.assign_book_to_student(request)
    
    @Books.post("/return_book_from_student")
    def return_book(request: BookSchema.ReturnBook,
                    service: IBookService = Book_Db_DI,
                    current_user: dict = Depends(require_role(["Admin"]))):
        return service.return_book_from_student(request)


    @Books.get("/pending_or_return_book")
    def pending_books(PendingBooks: Optional[str] = None,
                      ReturnBooks: Optional[str] = None,
                      service: IBookService = Book_Db_DI,
                      current_user: dict = Depends(require_role(["Admin"]))):
        return service.pending_or_return_book(PendingBooks, ReturnBooks)


    @Books.get("/get_record_by_author_id")
    def get_record_by_author_id(author_id: int, service: IBookService = Book_Db_DI,
                                current_user: dict = Depends(require_role(["Admin" , "Author"]))):
        return service.record_by_author_id(author_id)