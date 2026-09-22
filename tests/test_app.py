from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@example.com"

    first = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first.status_code == 200

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 200
    assert email not in response.json()["participants"]

    after = client.get("/activities")
    assert email not in after.json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/participants?email=missing@example.com")
    assert response.status_code == 404
