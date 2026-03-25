def test_create_expense(client, auth_headers):
    category_response = client.post("/api/categories", json={"name": "Transporte"}, headers=auth_headers)
    category_id = category_response.get_json()["data"]["id"]

    response = client.post(
        "/api/expenses",
        json={
            "category_id": category_id,
            "amount": "100.50",
            "description": "Uber",
            "spent_at": "2026-03-11T08:30:00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["data"]["amount"] == "100.50"
