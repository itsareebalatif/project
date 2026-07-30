def test_group_balances(client):
  # Register user
  client.post(
      "/auth/register",
      json={"name": "User 1", "email": "u1@example.com", "password": "123"},
  )
  token = client.post(
      "/auth/login", data={"username": "u1@example.com", "password": "123"}
  ).json()["access_token"]
  headers = {"Authorization": f"Bearer {token}"}

  # Create group
  group_id = client.post(
      "/groups", json={"name": "Test Group"}, headers=headers
  ).json()["id"]

  # Check balances endpoint responds with 200
  res = client.get(f"/groups/{group_id}/balances", headers=headers)
  assert res.status_code == 200
  assert isinstance(res.json(), list)