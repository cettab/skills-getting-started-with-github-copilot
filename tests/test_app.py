import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_duplicate():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # First signup should succeed
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp1.status_code == 200
    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400

def test_remove_participant():
    email = "removeuser@mergington.edu"
    activity = "Programming Class"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Remove participant
    resp = client.delete(f"/activities/{activity}/participant?email={email}")
    assert resp.status_code == 200
    # Removing again should fail
    resp2 = client.delete(f"/activities/{activity}/participant?email={email}")
    assert resp2.status_code == 404

def test_signup_nonexistent_activity():
    resp = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert resp.status_code == 404

def test_remove_nonexistent_participant():
    resp = client.delete("/activities/Chess Club/participant?email=notfound@mergington.edu")
    assert resp.status_code == 404
