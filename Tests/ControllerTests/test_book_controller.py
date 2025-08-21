from Controllers.main import app
from Database import get_db
from OAuthandJwt.JWTToken import verify_jwt
from Tests.MockDatabase.TestDatabase import override_get_db, override_verify_jwt_admin, client

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[verify_jwt] = override_verify_jwt_admin

#region CreateBook Endpoint
def test_create_book():
    create_book = \
        {
            "title": "Test6",
            "description": "Test6 string desc",
            "authorId": 1,
            "year": 2006
        }
    response = client.request("POST", "/create_book", json=create_book)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["title"] == "Test6"

def test_create_book_author_not_found():
    create_book = \
        {
            "title": "Test6",
            "description": "Test6 string desc",
            "authorId": 4, #Non-existence id
            "year": 2006
        }
    response = client.request("POST", "/create_book", json=create_book)
    assert response.status_code == 404
    assert "Author not found" in response.json()["detail"]

def test_create_book_already_exists():
    create_book = \
        {
            "title": "Test",
            "description": "Test6 string desc",
            "authorId": 1,
            "year": 2006
        }
    response = client.request("POST", "/create_book", json=create_book)
    assert response.status_code == 400
    assert "Book already exists" in response.json()["detail"]
#endregion CreateBook Endpoint

#region Assign_book_to_student
def test_assign_book_to_student():
    request =\
        {
    "book_id": 1,
    "title": "Test",
    "student_id": 1,
    "email": "test@test.com"
    }
    response = client.request("POST", "/assign_book_to_student", json=request)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 5
    assert data["Student_Name"] == "Sameer"

def test_assign_to_student_book_not_found():
    request =\
        {
    "book_id": 5,
    "title": "Test",
    "student_id": 1,
    "email": "test@test.com"
    }
    response = client.request("POST", "/assign_book_to_student", json=request)
    assert response.status_code == 404
    assert "Book not found" in response.json()["detail"]

def test_assign_to_student_not_found():
    request =\
        {
    "book_id": 1,
    "title": "Test",
    "student_id": 6,
    "email": "test@test.com"
    }
    response = client.request("POST", "/assign_book_to_student", json=request)
    assert response.status_code == 404
    assert "Student not found" in response.json()["detail"]

def test_assign_to_student_book_already_assigned_to_student():
    request =\
        {
    "book_id": 2,
    "title": "Test 2",
    "student_id": 2,
    "email": "test2@test.com"
    }
    response = client.request("POST", "/assign_book_to_student", json=request)
    assert response.status_code == 400
    assert "Book already assigned to student" in response.json()["detail"]
#endregion Assign_book_to_student

#region ReturnBook from Student
def test_return_book_from_student():
    request=\
        {
    "title": "Test",
    "email": "test@test.com"
    }
    response = client.request("POST", "/return_book_from_student", json=request)
    assert response.status_code == 200
    data = response.json()
    assert data == "ThankYou 'Sameer' for using book 'Test'"

def test_return_book_from_student_details_not_found():
    request=\
        {
    "title": "Test10",
    "email": "test10@test.com"
    }
    response = client.request("POST", "/return_book_from_student", json=request)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Enter details not found"

def test_return_book_from_student_already_returned():
    request=\
        {
    "title": "Test 2",
    "email": "test2@test.com"
    }
    response = client.request("POST", "/return_book_from_student", json=request)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Book already returned or details not found"
#endregion ReturnBook from Student

#region Pending or Return book
def test_return_books_from_student():
    response= client.get("/pending_or_return_book?ReturnBooks=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["Student_name"] == "Sameer2"
    assert data[0]["Book_title"] == "Test 2"

def test_pending_books_from_student():
    response= client.get("/pending_or_return_book?PendingBooks=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["Student_name"] == "Sameer"
    assert data[0]["Book_title"] == "Test"

def test_pending_books_and_return_books_from_student():
    response= client.get("/pending_or_return_book?ReturnBooks=1&PendingBooks=1")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Use only 1 option"
#endregion Pending or Return book

#region All books accord to Author id
def test_get_record_by_author_id():
    author_id =2
    response = client.get(f"/get_record_by_author_id?author_id={author_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["author_id"] == author_id
    assert data[0]["Author Name"] == "Author Two"
    assert data[0]["Author Nationality"] == "American"

def test_get_record_by_author_id_not_found():
    author_id =5
    response = client.get(f"/get_record_by_author_id?author_id={author_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Author not found"
#endregion All books accord to Author id