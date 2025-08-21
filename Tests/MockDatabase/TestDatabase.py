from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from Controllers.main import app
from Models.Author import Author as AuthorModel
from Models.Books import Book as BookModel
from Models.Student import Student as StudentModel
from Models.StudentBook import StudentBook as StudentBookModel
from Tests.MockDatabase.MockFilter import make_filter_side_effect
from Tests.Models.TestModels import MOCK_Author, MOCK_BOOK, MOCK_STUDENTS, MOCK_STUDENT_BOOK

client = TestClient(app)


def override_get_db():
    db = MagicMock()

    def query_side_effect(model):
        mock_query = MagicMock()
        if model is AuthorModel:
            mock_query.all.return_value = MOCK_Author
            mock_query.filter.side_effect = make_filter_side_effect(MOCK_Author)
        elif model is BookModel:
            mock_query.all.return_value = MOCK_BOOK
            mock_query.filter.side_effect = make_filter_side_effect(MOCK_BOOK)
        elif model is StudentModel:
            mock_query.all.return_value = MOCK_STUDENTS
            mock_query.filter.side_effect = make_filter_side_effect(MOCK_STUDENTS)
        elif model is StudentBookModel:
            mock_query.all.return_value = MOCK_STUDENT_BOOK
            mock_query.filter.side_effect = make_filter_side_effect(MOCK_STUDENT_BOOK)
        else:
            mock_query.all.return_value = []
            mock_query.filter.return_value.first.return_value = None

        return mock_query

    db.query.side_effect = query_side_effect
    db.delete.return_value = None
    db.commit.return_value = None

    yield db



def override_verify_jwt_admin():
    return {"role": "Admin", "sub": "testuser@gmail.com"}


def override_verify_jwt_forbidden():
    return {"role": "User", "sub": "testuser@gmail.com"}
