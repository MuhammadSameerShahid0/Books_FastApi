from sqlalchemy.orm import Session

from Factory.InterfaceAbstractFactory.IAbstractFactory import IAbstractFactory
from Factory.RegistryFactory import ServiceFactory
from Interfaces.IAuthService import IAuthService
from Interfaces.IAuthorService import IAuthorService
from Interfaces.IBookService import IBookService
from Interfaces.ICompleteStdDetailsService import ICompleteStdDetailsService
from Interfaces.IGoogle2FAService import IGoogle2FAService
from Interfaces.IStudentProfileService import IStudentProfileService
from Interfaces.IStudentService import IStudentService


class PostgresServiceFactory(IAbstractFactory):
    def create_book_service(self, db: Session) -> IBookService:
        return ServiceFactory.get_services("book", db)

    def create_auth_service(self, db: Session) -> IAuthService:
        return ServiceFactory.get_services("auth", db)

    def create_author_service(self, db: Session) -> IAuthorService:
        return ServiceFactory.get_services("author", db)

    def create_compltestddetails_service(self, db: Session) -> ICompleteStdDetailsService:
        return ServiceFactory.get_services("stddetails", db)

    def create_google2fa_service(self, db: Session) -> IGoogle2FAService:
        return ServiceFactory.get_services("google2fa", db)

    def create_student_service(self, db: Session) -> IStudentService:
        return ServiceFactory.get_services("student", db)

    def create_stdprofile_service(self, db: Session) -> IStudentProfileService:
        return ServiceFactory.get_services("studentprofile", db)
