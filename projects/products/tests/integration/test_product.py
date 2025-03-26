from fastapi.testclient import TestClient

product_payload = {
    "id": 1,
    "name": "product A",
    "category": "A",
    "price": 10,
    "stock": 2
}

def test_create_product(client: TestClient):
    response_created = client.post(url=f"/api/products", json=product_payload)
    assert response_created.status_code == 200

    response_get = client.get(url=f"/api/products/{product_payload["id"]}")
    json_payload = response_get.json()
    assert response_get.status_code == 200
    assert json_payload["id"] == product_payload["id"]
    assert json_payload["name"] == product_payload["name"]
    assert json_payload["category"] == product_payload["category"]
    assert json_payload["price"] == product_payload["price"]
    assert json_payload["stock"] == product_payload["stock"]
