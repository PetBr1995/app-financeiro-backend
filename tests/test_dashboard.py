def test_monthly_dashboard_summary(client, auth_headers):
    category_response = client.post("/api/categories", json={"name": "Alimentação"}, headers=auth_headers)
    category_id = category_response.get_json()["data"]["id"]

    client.post(
        "/api/incomes",
        json={
            "amount": "3000.00",
            "description": "Freela",
            "received_at": "2026-03-05T12:00:00",
        },
        headers=auth_headers,
    )

    client.post(
        "/api/expenses",
        json={
            "category_id": category_id,
            "amount": "450.00",
            "description": "Supermercado",
            "spent_at": "2026-03-06T09:00:00",
        },
        headers=auth_headers,
    )

    response = client.get("/api/dashboard/summary?month=3&year=2026", headers=auth_headers)
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["total_incomes"] == "3000.00"
    assert body["data"]["total_expenses"] == "450.00"
    assert body["data"]["balance"] == "2550.00"
    assert body["data"]["expenses_by_category"][0]["category"] == "Alimentação"
