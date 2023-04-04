from datetime import datetime

from app.crud import create_user, create_group
from app.schemas import UserCreate, GroupCreate

def check_created_at_field_helper(data):
    """ Helper function to check if the 'created_at' field is present and has a valid date-time format """
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


def create_user_helper(SessionLocal):
    """ Helper function to create a user """
    db = SessionLocal()
    user_in = UserCreate(name="test", email="test@gmail.com", password="test")
    return create_user(db, user_in)


def create_group_helper(SessionLocal):
    """ Helper function to create a group """
    db = SessionLocal()
    group_in = GroupCreate(name="test", description="hogehogehogege", creator_id=1)
    return create_group(db, group_in)