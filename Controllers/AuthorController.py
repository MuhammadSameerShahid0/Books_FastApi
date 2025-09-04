from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from Database import get_db
from Factory.AbstractFactory import PostgresServiceFactory
from Factory.RegistryFactory import ServiceFactory
from Interfaces.IAuthorService import IAuthorService
from OAuthandJwt.JWTToken import require_role
from Services.AuthorService import AuthorService

app = FastAPI()
Author = APIRouter(tags=["Author"])
service_factory = PostgresServiceFactory()

def get_author_service(db: Session = Depends(get_db)) -> IAuthorService:
    return service_factory.create_author_service(db)

Author_Db_DI = Depends(get_author_service)

class AuthorController:
    @Author.get('/get_author')
    async def get_author_list(services : IAuthorService = Author_Db_DI,
                        current_user: dict = Depends(require_role(["Admin"]))):
        return await services.author_list()

    @Author.get('/author_list_and_books')
    def get_author_list_and_books(services : IAuthorService = Author_Db_DI,
                                  current_user: dict = Depends(require_role(["Admin" , "Student", "Author"]))):
        return services.author_list_and_books()

    @Author.delete('/author_id')
    def delete_author_id(author_id: int,
                         service : IAuthorService = Author_Db_DI,
                         current_user: dict = Depends(require_role(["Admin"]))):
        return service.delete_author(author_id)

