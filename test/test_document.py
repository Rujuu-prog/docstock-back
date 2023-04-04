from fastapi.testclient import TestClient

from app.main import app
from . import decorator
from .utils import check_created_at_field_helper, create_user_helper ,create_group_helper, create_document_helper

client = TestClient(app)


@decorator.temp_db
def test_create_document(SessionLocal):
    # Create test user using the helper function
    test_user = create_user_helper(SessionLocal)
    test_group = create_group_helper(SessionLocal)
    document_data = {
        "title": "test",
        "content": "#aaa"
    }

    response = client.post(
        f"/documents?owner_id={test_user.id}&group_id={test_group.id}",
        json=document_data,)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Error details: {response.text}"
    data = response.json()
    assert "id" in data
    assert data["title"] == document_data["title"]
    assert data["content"] == document_data["content"]
    assert data["owner_id"] == test_user.id
    assert data["group_id"] == test_group.id
    check_created_at_field_helper(data)


@decorator.temp_db
def test_get_document(SessionLocal):
    # Create test document using the helper function
    test_user = create_user_helper(SessionLocal)
    test_group = create_group_helper(SessionLocal)
    test_document = create_document_helper(SessionLocal, test_user.id, test_group.id)

    # Test the GET endpoint
    response = client.get(f"/documents/{test_document.id}")

    # Verify the response status code and data
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Error details: {response.text}"
    data = response.json()
    assert data["id"] == test_document.id
    assert data["title"] == "test"
    assert data["content"] == "#aaa"
    assert data["owner_id"] == test_user.id
    assert data["group_id"] == test_group.id
    check_created_at_field_helper(data)