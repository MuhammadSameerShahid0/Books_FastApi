from abc import ABC, abstractmethod
from typing import List
from Schema.StudentProfileSchema import UpdateProfile


class IStudentProfileService(ABC):

    @abstractmethod
    def update_student_profile(self, request: UpdateProfile):
        pass

    @abstractmethod
    def list_of_student_profile(self) -> List:
        pass

    @abstractmethod
    def student_by_id(self, student_id: int):
        pass