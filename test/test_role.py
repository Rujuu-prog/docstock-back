from fastapi.testclient import TestClient

from app.main import app
from . import decorator
from .utils import create_role_helper

client = TestClient(app)

@decorator.temp_db
def test_get_role(SessionLocal):
    # Create test role using the helper function
    test_role = create_role_helper(SessionLocal)
    # Test the GET endpoint
    response = client.get(f"/roles/{1}")
    # Verify the response status code and data
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Error details: {response.text}"
    data = response.json()
    assert data["id"] == test_role.id
    assert data["name"] == "test"