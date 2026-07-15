from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def setup_function():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]


def test_unregister_participant_removes_email_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    activities_data = activities_response.json()["Chess Club"]
    assert "michael@mergington.edu" not in activities_data["participants"]


def test_unregister_participant_returns_404_for_unknown_activity():
    response = client.delete("/activities/Unknown Activity/participants/student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
