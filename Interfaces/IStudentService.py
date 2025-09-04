from abc import ABC, abstractmethod
from typing import List
from Schema import StudentSchema
from Models.Student import Student as StudentModel


class IStudentService(ABC):

    @abstractmethod
    def student_list(self) -> List[StudentModel]:
        pass

    @abstractmethod
    def student_by_id(self, student_id: int) -> StudentModel:
        pass

    @abstractmethod
    def student_is_true(self) -> List[StudentModel]:
        pass

    @abstractmethod
    def update_Student(self,
                       student_id: int,
                       email: str,
                       request: StudentSchema.StudentUpdate) -> StudentModel:
        pass

    @abstractmethod
    def delete_Student(self, request: StudentSchema.StudentDelete) -> str:
        pass