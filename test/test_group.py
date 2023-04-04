from fastapi.testclient import TestClient

from app.main import app
from . import decorator
from .utils import check_created_at_field_helper, create_user_helper ,create_group_helper

client = TestClient(app)


@decorator.temp_db
def test_create_group(SessionLocal):
    # Create test user using the helper function
    test_user = create_user_helper(SessionLocal)

    response = client.post(
        "/groups/",
        json={
            "name": "test",
            "description": "hogehogehogege",
            "creator_id": test_user.id,
        },)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Error details: {response.text}"
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "test"
    assert data["description"] == "hogehogehogege"
    check_created_at_field_helper(data)


@decorator.temp_db
def test_get_group(SessionLocal):
    # Create test group using the helper function
    test_group = create_group_helper(SessionLocal)

    # Test the GET endpoint
    response = client.get(f"/groups/{test_group.id}")

    # Verify the response status code and data
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Error details: {response.text}"
    data = response.json()
    assert data["id"] == test_group.id
    assert data["name"] == "test"
    assert data["description"] == "hogehogehogege"
    check_created_at_field_helper(data)