from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.testing import skip_if
from starlette import status
from Models.Books import Book as BookModel
from Database import get_db
from Schema import AuthorSchema
from Models.Author import Author as AuthorModel

app = FastAPI()
Author = APIRouter(tags=["Author"])


class AuthorController:
    @Author.post('/register_author')
    def register_author(requets: AuthorSchema.CreateAuthor, db: Session = Depends(get_db)):
        try:
            verify_email_exists = db.query(AuthorModel).filter(AuthorModel.email == requets.email).first()
            if verify_email_exists:
                raise HTTPException(status_code=400, detail="Author already registered")

            register_author = AuthorModel(**requets.model_dump())
            db.add(register_author)
            db.commit()
            db.refresh(register_author)
            return register_author

        except Exception as ex:
            db.rollback()
            code = getattr(500, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )
        finally:
            db.close()

    @Author.get('/get_author')
    def get_author_list(db: Session = Depends(get_db)):
        return db.query(AuthorModel).all()

    @Author.get('/author_list_and_books')
    def get_author_list_and_books(db: Session = Depends(get_db)):
        try:
            get_authors_list = db.query(AuthorModel).all()
            if get_authors_list:
                result = []
                for author in get_authors_list:
                    get_books_list = db.query(BookModel).filter(BookModel.author_id == author.id).first()

                    result_record = {
                        **author.__dict__,
                        "Book title": get_books_list.title if get_books_list else None,
                        "Book Year": get_books_list.year if get_books_list else None,
                    }

                    result.append(result_record)

                return result
            else:
                raise HTTPException(status_code=404, detail="Author's not found")

        except Exception as ex:
            code = getattr(500, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            raise HTTPException(
                           status_code=code,
                detail=str(ex)
            )

    @Author.delete('/author_id')
    def delete_author_id(author_id: int, db: Session = Depends(get_db)):
        try:
            verify_id = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
            if verify_id:
                db.delete(verify_id)
                db.commit()
                return f"Author '{verify_id.name}' deleted"
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
        finally:
            db.close()

