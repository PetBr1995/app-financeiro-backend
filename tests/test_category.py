def test_create_category(client, auth_headers):
    response = client.post("/api/categories", json={"name": "Moradia"}, headers=auth_headers)

    assert response.status_code == 201
    body = response.get_json()
    assert body["data"]["name"] == "Moradia"
