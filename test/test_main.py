from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app
from . import decorator

client = TestClient(app)

@decorator.temp_db
def test_create_user():
    response = client.post(
        "/users/",
        json={
            "name": "test",
            "email": "test@gmail.com",
            "password": "test",
        },)
    if response.status_code != 200:
        print("Error details:", response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "test"
    assert data["email"] == "test@gmail.com"
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