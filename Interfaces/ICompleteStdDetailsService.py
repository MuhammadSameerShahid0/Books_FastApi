from abc import ABC, abstractmethod
from typing import Optional, List
from Schema.StdDetailsSchema import StdDetailsSchema


class ICompleteStdDetailsService(ABC):

    @abstractmethod
    def std_details(self, student_id: int) -> List[StdDetailsSchema]:
        pass

    @abstractmethod
    def pending_or_return(self,
                          student_id: int,
                          pending: Optional[str] = None,
                          Return: Optional[str] = None) -> List[StdDetailsSchema]:
        pass