from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from FileLogging.SimpleLogging import simplelogging
from Interfaces.IAuthorService import IAuthorService
from Models.Author import Author as AuthorModel
from Models.Books import Book as BookModel

logger = simplelogging("AuthorService")

class AuthorService(IAuthorService):
    def __init__(self, db: Session):
        self.db = db

    async def author_list(self):
        logger.info(f"'Admin' tries to getting the author list and they successfully got the author list")
        return self.db.query(AuthorModel).all()

    def author_list_and_books(self):
        try:
            get_authors_list = self.db.query(AuthorModel).all()
            if get_authors_list:
                result = []
                for author in get_authors_list:
                    get_books_list = self.db.query(BookModel).filter(BookModel.author_id == author.id).first()

                    result_record = {
                        **author.__dict__,
                        "Book title": get_books_list.title if get_books_list else None,
                        "Book Year": get_books_list.year if get_books_list else None,
                    }

                    result.append(result_record)
                    logger.info(f"Author list with book successfully returned")

                return result
            else:
                raise HTTPException(status_code=404, detail="Author's not found")

        except Exception as ex:
            code = getattr(500, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex

            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )

    def delete_author(self, author_id: int):
        try:
            verify_id = self.db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
            if verify_id:
                self.db.delete(verify_id)
                self.db.commit()
                logger.info(f"'Admin', deleted the Author {author_id} successfully")
                return f"Author '{verify_id.name}' deleted"
            else:
                raise HTTPException(status_code=404, detail="Author not found")
        except Exception as ex:
            code = getattr(ex, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
            if isinstance(ex, HTTPException):
                raise ex
            logger.error(f"Something went wrong, error code is {code} and error details is {ex}")

            raise HTTPException(
                status_code=code,
                detail=str(ex)
            )