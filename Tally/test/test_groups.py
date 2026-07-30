def test_create_and_access_group(client):
  # first signup and then login and then create
  client.post(
      "/auth/register",
      json={
          "name": "Sara",
          "email": "sara@example.com",
          "password": "password123",
      },
  )
  token = client.post(
      "/auth/login",
      data={"username": "sara@example.com", "password": "password123"},
  ).json()["access_token"]
  headers = {"Authorization": f"Bearer {token}"}

  # Create 
  res = client.post("/groups", json={"name": "Flatmates"}, headers=headers)
  assert res.status_code == 201
  assert res.json()["name"] == "Flatmates"