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


def test_balances_sum_to_zero(client):
  # Register two users: one who pays, one who owes
  payer = client.post(
      "/auth/register",
      json={"name": "Payer", "email": "payer@example.com", "password": "123"},
  ).json()
  ower = client.post(
      "/auth/register",
      json={"name": "Ower", "email": "ower@example.com", "password": "123"},
  ).json()

  token = client.post(
      "/auth/login", data={"username": "payer@example.com", "password": "123"}
  ).json()["access_token"]
  headers = {"Authorization": f"Bearer {token}"}

  # Payer creates the group and adds the ower as a member
  group_id = client.post(
      "/groups", json={"name": "Trip"}, headers=headers
  ).json()["id"]
  client.post(
      f"/groups/{group_id}/members",
      json={"user_id": ower["id"]},
      headers=headers,
  )

  # Payer pays 1000 cents, split evenly between the two members
  client.post(
      f"/groups/{group_id}/expenses",
      json={
          "description": "Lunch",
          "amount_cents": 1000,
          "splits": [
              {"user_id": payer["id"], "share_cents": 500},
              {"user_id": ower["id"], "share_cents": 500},
          ],
      },
      headers=headers,
  )

  balances = client.get(f"/groups/{group_id}/balances", headers=headers).json()

  # Money isn't created or destroyed: everyone's net balance must add up to zero
  total_net_cents = sum(member["net_cents"] for member in balances)
  assert total_net_cents == 0

  # And the payer should be owed exactly what the ower owes them
  net_by_user = {member["user_id"]: member["net_cents"] for member in balances}
  assert net_by_user[payer["id"]] == 500
  assert net_by_user[ower["id"]] == -500