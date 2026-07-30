def test_splits_must_sum_rule(client):
  # Register & login
  client.post(
      "/auth/register",
      json={
          "name": "Ahmed",
          "email": "ahmed@example.com",
          "password": "password123",
      },
  )
  token = client.post(
      "/auth/login",
      data={"username": "ahmed@example.com", "password": "password123"},
  ).json()["access_token"]
  headers = {"Authorization": f"Bearer {token}"}

  # Create group
  group_id = client.post(
      "/groups", json={"name": "Dinner Trip"}, headers=headers
  ).json()["id"]

  # Bad expense: amount is 3000, but splits only add up to 2000 (Should trigger 422)
  payload = {
      "description": "Pizza",
      "amount_cents": 3000,
      "category": "Food",
      "paid_by": 1,
      "splits": [{"user_id": 1, "share_cents": 1000}, {"user_id": 1, "share_cents": 1000}],
  }
  res = client.post(
      f"/groups/{group_id}/expenses", json=payload, headers=headers
  )
  assert res.status_code == 422