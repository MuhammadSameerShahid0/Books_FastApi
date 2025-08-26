from abc import ABC, abstractmethod
from typing import Optional, List, Any
from Schema import BookSchema
from Schema.BookSchema import ResponseAssignBookToStudent


class IBookService(ABC):

    @abstractmethod
    async def create_book(self, request: BookSchema.CreateBook) -> Any:
        pass

    @abstractmethod
    def assign_book_to_student(self, request: BookSchema.AssignBookToStudent) -> ResponseAssignBookToStudent:
        pass

    @abstractmethod
    def return_book_from_student(self, request: BookSchema.ReturnBook) -> str:
        pass

    @abstractmethod
    def pending_or_return_book(self,
                               PendingBooks: Optional[str] = None,
                               ReturnBooks: Optional[str] = None) -> List[Any]:
        pass

    @abstractmethod
    def record_by_author_id(self, author_id: int) -> List[Any]:
        pass