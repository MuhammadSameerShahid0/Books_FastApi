# Services/IAuthorService.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IAuthorService(ABC):

    @abstractmethod
    async def author_list(self) -> List[Any]:
        pass

    @abstractmethod
    def author_list_and_books(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_author(self, author_id: int) -> str:
        pass