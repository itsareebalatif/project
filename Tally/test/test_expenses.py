def test_expense_list_filters_by_date_range(client):
  from datetime import datetime
  from test.conftest import TestingSessionLocal
  from app import models

  # Register & login
  client.post(
      "/auth/register",
      json={"name": "Sara", "email": "sara@example.com", "password": "password123"},
  )
  token = client.post(
      "/auth/login",
      data={"username": "sara@example.com", "password": "password123"},
  ).json()["access_token"]
  headers = {"Authorization": f"Bearer {token}"}

  group_id = client.post(
      "/groups", json={"name": "Roommates"}, headers=headers
  ).json()["id"]

  # Two expenses, both created "now" by the API - we'll backdate one below
  old_expense = client.post(
      f"/groups/{group_id}/expenses",
      json={
          "description": "Old rent",
          "amount_cents": 1000,
          "splits": [{"user_id": 1, "share_cents": 1000}],
      },
      headers=headers,
  ).json()
  client.post(
      f"/groups/{group_id}/expenses",
      json={
          "description": "Recent groceries",
          "amount_cents": 500,
          "splits": [{"user_id": 1, "share_cents": 500}],
      },
      headers=headers,
  )

  # The API has no way to backdate an expense, so push "Old rent" into the
  # past directly through the DB to actually exercise the date filter
  db = TestingSessionLocal()
  db.query(models.Expense).filter_by(id=old_expense["id"]).update(
      {"created_at": datetime(2020, 1, 1)}
  )
  db.commit()
  db.close()

  res = client.get(
      f"/groups/{group_id}/expenses?start_date=2020-01-01&end_date=2020-01-02",
      headers=headers,
  )
  assert res.status_code == 200
  descriptions = [e["description"] for e in res.json()]
  assert descriptions == ["Old rent"]

  # A range that excludes 2020 should only pick up the recent expense
  res = client.get(
      f"/groups/{group_id}/expenses?start_date=2025-01-01",
      headers=headers,
  )
  assert [e["description"] for e in res.json()] == ["Recent groceries"]


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