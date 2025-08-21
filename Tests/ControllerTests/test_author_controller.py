from Controllers.main import app
from Database import get_db
from OAuthandJwt.JWTToken import verify_jwt
from Tests.MockDatabase.TestDatabase import override_verify_jwt_admin, client, \
    override_verify_jwt_forbidden, override_get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[verify_jwt] = override_verify_jwt_admin

def test_get_author_list():
    response = client.get('/get_author')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["name"] == "Author One"

def test_get_author_list_forbidden():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_forbidden

    response = client.get('/get_author')
    assert response.status_code == 403
    assert "permission" in response.json()["detail"].lower()

def test_delete_author_id():
    author_id = 1
    response = client.request('DELETE', f'/author_id?author_id={author_id}')
    assert response.status_code == 200
    data = response.json()
    assert data == "Author 'Author One' deleted"

def test_author_not_found_delete_author_id():
    non_existence_id = 999
    response = client.request('DELETE', f'/author_id?author_id={non_existence_id}')
    assert response.status_code == 404
    assert "Author not found" in response.json()["detail"]

def test_get_author_list_and_books_success():
    response = client.get('/author_list_and_books')

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["Book title"] == "Test"
    assert data[1]["Book title"] == "Test 2"
