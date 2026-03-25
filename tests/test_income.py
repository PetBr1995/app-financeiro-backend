def test_create_income(client, auth_headers):
    response = client.post(
        "/api/incomes",
        json={
            "amount": "2500.00",
            "description": "Salário",
            "received_at": "2026-03-10T10:00:00",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["data"]["amount"] == "2500.00"
