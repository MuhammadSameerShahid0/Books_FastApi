from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from Interfaces.IAuthService import IAuthService
from Interfaces.IAuthorService import IAuthorService
from Interfaces.IBookService import IBookService
from Interfaces.ICompleteStdDetailsService import ICompleteStdDetailsService
from Interfaces.IGoogle2FAService import IGoogle2FAService
from Interfaces.IStudentProfileService import IStudentProfileService
from Interfaces.IStudentService import IStudentService


class IAbstractFactory(ABC):
    @abstractmethod
    def create_auth_service(self, db: Session) -> IAuthService:
        pass

    @abstractmethod
    def create_author_service(self, db: Session) -> IAuthorService:
        pass

    @abstractmethod
    def create_book_service(self, db : Session) -> IBookService:
        pass

    @abstractmethod
    def create_compltestddetails_service(self, db: Session) -> ICompleteStdDetailsService:
        pass

    @abstractmethod
    def create_google2fa_service(self, db: Session) -> IGoogle2FAService:
        pass

    @abstractmethod
    def create_student_service(self, db: Session) -> IStudentService:
        pass

    @abstractmethod
    def create_stdprofile_service(self, db: Session) -> IStudentProfileService:
        pass