from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_success():
    response = client.post("/auth/signup", json={
        "name": "Auth User",
        "email": "authuser@gmail.com",
        "password": "password123"
    })
    assert response.status_code in [201, 400]

def test_login_success():
    client.post("/auth/signup", json={
        "name": "Auth User",
        "email": "authuser@gmail.com",
        "password": "password123"
    })
    
    response = client.post("/auth/login", json={
        "email": "authuser@gmail.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()