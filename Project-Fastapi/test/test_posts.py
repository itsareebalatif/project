from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_create_post():
    # Login 
    login_response = client.post("/auth/login", json={
        "email": "testuser@gmail.com",
        "password": "password123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a post
    response = client.post("/posts/", json={
        "title": "My First Test Post",
        "content": "Hello World!"
    }, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My First Test Post"
    assert "id" in data

def test_cannot_edit_someone_else_post():
    client.post("/auth/signup", json={
        "name": "User One",
        "email": "user1@gmail.com",
        "password": "password123"
    })
    login1 = client.post("/auth/login", json={
        "email": "user1@gmail.com",
        "password": "password123"
    })
    token1 = login1.json()["access_token"]
    
    post_res = client.post("/posts/", json={
        "title": "User 1's Secret Post",
        "content": "Hands off!"
    }, headers={"Authorization": f"Bearer {token1}"})
    post_id = post_res.json()["id"]

    #  signup and login for unauthorize ---
    client.post("/auth/signup", json={
        "name": "User Two (Hacker)",
        "email": "user2@gmail.com",
        "password": "password123"
    })
    login2 = client.post("/auth/login", json={
        "email": "user2@gmail.com",
        "password": "password123"
    })
    token2 = login2.json()["access_token"]

    # unotherize trying to update
    update_res = client.put(f"/posts/{post_id}", json={
        "title": "Hacked Title",
        "content": "Rewritten by User 2"
    }, headers={"Authorization": f"Bearer {token2}"})

    # will gv error
    assert update_res.status_code == 403