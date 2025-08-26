from abc import ABC, abstractmethod
from typing import Optional
from starlette.requests import Request
from Schema import StudentSchema, AuthorSchema
from Schema.AuthSchema import Token


class IAuthService(ABC):

    @abstractmethod
    async def google_register(self, request: Request):
        pass

    @abstractmethod
    async def google_callback(self, request: Request) -> Token:
        pass

    @abstractmethod
    async def register_student(self, request: StudentSchema.StudentCreate) -> StudentSchema.StudentResponse:
        pass

    @abstractmethod
    async def register_author(self, request: AuthorSchema.CreateAuthor):
        pass

    @abstractmethod
    async def google_login(self, email: str, otp: Optional[str] = None) -> Token:
        pass

    @abstractmethod
    def login(self, email: str, otp: Optional[str] = None) -> Token:
        pass