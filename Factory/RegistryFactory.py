from sqlalchemy.orm import Session

from Services.AuthService import AuthService
from Services.AuthorService import AuthorService
from Services.BookService import BookService
from Services.CompleteStdDetailsService import CompleteStdDetailsService
from Services.EmailService import EmailService
from Services.Google2FAService import Google2FAService
from Services.StudentProfileService import StudentProfileService
from Services.StudentService import StudentService


class ServiceFactory:

    _services = {
        "book" : BookService,
        "author" : AuthorService,
        "auth" : AuthService,
        "stddetails" : CompleteStdDetailsService,
        "google2fa" : Google2FAService,
        "studentprofile" : StudentProfileService,
        "student" : StudentService,
    }

    def get_services(service_type : str, db : Session):
        service_cls = ServiceFactory._services.get(service_type.lower())
        if not service_cls:
            raise Exception(f"Service type {service_type} is not supported")
        if service_type == "auth":
            email_service = EmailService()
            return service_cls(db, email_service)
        return service_cls(db)