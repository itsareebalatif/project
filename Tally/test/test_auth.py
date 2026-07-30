def test_register_and_login(client):
  # test for signupppp
  response = client.post(
      "/auth/register",
      json={
          "name": "Ali",
          "email": "ali@example.com",
          "password": "password123",
      },
  )
  assert response.status_code == 201
  assert response.json()["email"] == "ali@example.com"

  # Login t
  login_res = client.post(
      "/auth/login", data={"username": "ali@example.com", "password": "password123"}
  )
  assert login_res.status_code == 200
  assert "access_token" in login_res.json()