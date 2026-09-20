import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert delete_response.status_code == 200
    assert "Unregistered" in delete_response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
