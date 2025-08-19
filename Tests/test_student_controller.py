from Controllers.main import app
from OAuthandJwt.JWTToken import verify_jwt
from Database import get_db
from Tests.TestDatabase import client, create_mock_db, override_verify_jwt_admin, override_verify_jwt_forbidden

mock_db = create_mock_db()
app.dependency_overrides[get_db] = lambda: mock_db

def test_get_student_list_success():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_admin

    response = client.get("/student_list")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["name"] == "Sameer"
    assert data[0]["email"] == "test@test.com"

def test_get_student_list_forbidden():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_forbidden

    response = client.get("/student_list")

    assert response.status_code == 403
    assert "permission" in response.json()["detail"].lower()

def test_get_student_by_id_found():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_admin
    student_id = 1

    response = client.get(f"/student_by_id?student_id={student_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == student_id
    assert data["email"] == "test@test.com"

def test_get_student_by_id_not_found():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_admin
    non_existent_id = 999

    response = client.get(f"/student_by_id?student_id={non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_is_student_true():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_admin

    response = client.get("/IsStudent_True")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["IsStudent"] is True

def test_update_student_if_is_student_true():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_admin

    student_id = 2
    email = "test2@test.com"
    update_item =\
        {
          "name": "Error's Fixed",
          "age": 12,
          "new_email" : "test4@test.com"
        }
    response = client.post(f"/Update_Student_If_IsStudent_True?student_id={student_id}&email={email}", json=update_item)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_item["name"]
    assert data["email"] == update_item["new_email"]

def test_email_already_exist_update_student_if_is_student_true():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_admin

    student_id = 2
    email = "test2@test.com"
    update_item = \
        {
            "name": "Error's Fixed",
            "age": 12,
            "new_email": "test3@test.com"
        }
    response = client.post(f"/Update_Student_If_IsStudent_True?student_id={student_id}&email={email}", json=update_item)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_std_not_active_update_student_if_is_student_true():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_admin

    student_id = 3
    email = "test3@test.com"
    update_item = \
        {
            "name": "Error's Fixed",
            "age": 12,
            "new_email": "test5@test.com"
        }
    response = client.post(f"/Update_Student_If_IsStudent_True?student_id={student_id}&email={email}", json=update_item)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not active"

def test_delete_student_by_id():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_admin

    delete_request=\
        {
        "id": 1,
        "email": "test@test.com"
        }
    response = client.request( "DELETE", "/Delete_Student_By_id", json=delete_request)
    assert response.status_code == 200
    data = response.json()
    assert data == "Student deleted successfully. Id : 1 name : Sameer"

def test_email_not_correct_delete_student_by_id():
    app.dependency_overrides[verify_jwt] = override_verify_jwt_admin

    delete_request=\
        {
        "id": 1,
        "email": "test2@test.com"
        }
    response = client.request( "DELETE", "/Delete_Student_By_id", json=delete_request)
    assert response.status_code == 400
    data = response.json()
    assert response.json()["detail"] == "Email : 'test2@test.com' not correct against id : 1 ! Id not correct against email : 'test2@test.com'"