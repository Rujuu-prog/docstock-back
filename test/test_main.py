from fastapi.testclient import TestClient

from app.main import app
from app import crud, schemas
from . import decorator
from .utils import check_created_at_field_helper

client = TestClient(app)


@decorator.temp_db
def test_create_user(SessionLocal):
    response = client.post(
        "/users/",
        json={
            "name": "test",
            "email": "test@gmail.com",
            "password": "test",
        },)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Error details: {response.text}"
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "test"
    assert data["email"] == "test@gmail.com"
    check_created_at_field_helper(data)


def create_user_helper(SessionLocal):
    db = SessionLocal()
    user_in = schemas.UserCreate(name="test", email="test@gmail.com", password="test")
    return crud.create_user(db, user_in)

@decorator.temp_db
def test_get_user(SessionLocal):
    # Create test user using the helper function
    test_user = create_user_helper(SessionLocal)

    # Test the GET endpoint
    response = client.get(f"/users/{test_user.id}")

    # Verify the response status code and data
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Error details: {response.text}"
    data = response.json()
    assert data["id"] == test_user.id
    assert data["name"] == "test"
    assert data["email"] == "test@gmail.com"
    check_created_at_field_helper(data)