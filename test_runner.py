import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Debate Team" in data
    assert "participants" in data["Debate Team"]
    assert "max_participants" in data["Debate Team"]
    print("test_get_activities: PASSED")

def test_signup_success():
    # Use a unique email to avoid conflicts
    email = "test_signup@example.com"
    activity = "Debate Team"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result

    # Verify added
    response2 = client.get("/activities")
    data = response2.json()
    assert email in data[activity]["participants"]
    print("test_signup_success: PASSED")

def test_signup_already_signed_up():
    email = "test_duplicate@example.com"
    activity = "Debate Team"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Second signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    print("test_signup_already_signed_up: PASSED")

def test_signup_activity_not_found():
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404
    print("test_signup_activity_not_found: PASSED")

def test_unregister_success():
    email = "test_unregister@example.com"
    activity = "Math Club"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Then unregister
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result

    # Verify removed
    response2 = client.get("/activities")
    data = response2.json()
    assert email not in data[activity]["participants"]
    print("test_unregister_success: PASSED")

def test_unregister_not_signed_up():
    email = "test_not_signed@example.com"
    activity = "Math Club"
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response.status_code == 400
    print("test_unregister_not_signed_up: PASSED")

def test_unregister_activity_not_found():
    response = client.delete("/activities/NonExistent/participants?email=test@example.com")
    assert response.status_code == 404
    print("test_unregister_activity_not_found: PASSED")

if __name__ == "__main__":
    try:
        test_get_activities()
        test_signup_success()
        test_signup_already_signed_up()
        test_signup_activity_not_found()
        test_unregister_success()
        test_unregister_not_signed_up()
        test_unregister_activity_not_found()
        print("All tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)