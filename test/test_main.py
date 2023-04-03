from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app
from app import crud, schemas
from . import decorator

client = TestClient(app)

def check_created_at_field_helper(data):
    assert "created_at" in data, "The 'created_at' field is missing in the response"

    # Check if the 'created_at' field has a valid date-time format
    try:
        datetime.fromisoformat(data["created_at"])
    except ValueError:
        assert False, "Invalid date-time format in 'created_at' field"

    # Optionally, you can also check if the 'created_at' date-time is close to the current time
    # This ensures that the value of 'created_at' is a recent timestamp
    now = datetime.now()
    created_at = datetime.fromisoformat(data["created_at"])
    time_difference = now - created_at

    # Check if the 'created_at' timestamp is within an acceptable range (e.g., 5 seconds)
    assert time_difference.seconds < 5, "The 'created_at' timestamp is not recent"

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