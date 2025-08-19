from unittest.mock import Mock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from Controllers.main import app

client = TestClient(app)

class MockStudent:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

MOCK_STUDENTS = [
    MockStudent(id=1, name="Sameer", email="test@test.com", age=22, IsStudent=True, status_2fa=False, secret_2fa=None),
    MockStudent(id=2, name="Sameer2", email="test2@test.com", age=23, IsStudent=True, status_2fa=False, secret_2fa=None),
    MockStudent(id=3, name="Sameer3", email="test3@test.com", age=24, IsStudent=False, status_2fa=True, secret_2fa=None)
]


def create_mock_db():
    mock_db = Mock(spec=Session)

    class MockQuery:
        def __init__(self, data=None, conditions=None):
            self.data = data or MOCK_STUDENTS
            self.conditions = conditions or []

        def filter(self, *condition):
            return MockQuery(self.data, self.conditions + list(condition))

        def _apply_filters(self):
            filtered = self.data
            for cond in self.conditions:
                try:
                    field = cond.left.name
                    value = cond.right.value
                except AttributeError:
                    continue

                filtered = [s for s in filtered if str(getattr(s, field, None)) == str(value)]
            return filtered

        def first(self):
            filtered = self._apply_filters()
            return filtered[0] if filtered else None

        def all(self):
            return self._apply_filters()

    mock_db.query.return_value = MockQuery()
    return mock_db


def override_verify_jwt_admin():
    return {"role": "Admin", "sub": "testuser@gmail.com"}


def override_verify_jwt_forbidden():
    return {"role": "User", "sub": "testuser@gmail.com"}
