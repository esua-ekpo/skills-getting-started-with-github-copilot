import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original_participants = {
        name: list(details["participants"])
        for name, details in activities.items()
    }
    yield
    for name, details in activities.items():
        details["participants"] = list(original_participants[name])


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
