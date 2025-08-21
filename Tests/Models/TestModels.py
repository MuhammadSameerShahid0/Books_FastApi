from Models.Author import Author
from Models.Books import Book as BookModel
from Models.StudentBook import StudentBook as StudentBookModel

class StudentModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


MOCK_STUDENTS = [
    StudentModel(id=1, name="Sameer", email="test@test.com", age=22, IsStudent=True, status_2fa=False, secret_2fa=None),
    StudentModel(id=2, name="Sameer2", email="test2@test.com", age=23, IsStudent=True, status_2fa=False,
                 secret_2fa=None),
    StudentModel(id=3, name="Sameer3", email="test3@test.com", age=24, IsStudent=False, status_2fa=True,
                 secret_2fa=None)
]

MOCK_Author = [
        Author(
            id=1,
            name="Author One",
            email="one@example.com",
            bio="Bio for Author One",
            nationality="Pakistani",
            secret_2fa="secret1",
            status_2fa=True
        ),
        Author(
            id=2,
            name="Author Two",
            email="two@example.com",
            bio="Bio for Author Two",
            nationality="American",
            secret_2fa="secret2",
            status_2fa=False
        ),
        Author(
            id=3,
            name="Author Three",
            email="three@example.com",
            bio="Bio for Author Three",
            nationality="British",
            secret_2fa="secret3",
            status_2fa=True
        )
    ]

MOCK_BOOK = [
    BookModel(id=1, title="Test", description="Test string", year=2001, author_id=1),
    BookModel(id=2, title="Test 2", description="Test string 2", year=2002, author_id=2),
    BookModel(id=3, title="Test 3", description="Test string 3", year=2003, author_id=None)]


BookModel.author = MOCK_Author[0]

MOCK_STUDENT_BOOK = [
    StudentBookModel(id=1,AssignedAt="2025-08-11 21:20:42.115493",ReturnDate="2025-08-11 23:27:10.689777",
                     Status="Pending for Return", student_id=1,book_id=1),
    StudentBookModel(id=2,AssignedAt="2025-08-11 21:20:42.115493",ReturnDate="2025-08-11 23:27:10.689777",
                     Status="Return Successfully", student_id=2,book_id=2),
    StudentBookModel(id=3,AssignedAt="2025-08-11 21:20:42.115493",ReturnDate="2025-08-11 23:27:10.689777",
                     Status="Return Successfully", student_id=3,book_id=3),
    StudentBookModel(id=4,AssignedAt="2025-08-11 21:20:42.115493",ReturnDate="2025-08-11 23:27:10.689777",
                     Status="Pending for Return", student_id=3,book_id=1),
]
