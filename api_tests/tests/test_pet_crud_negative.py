import random


def test_get_nonexistent_pet_returns_404(api_session, base_url):
    missing_id = random.randint(9_000_000_000, 9_999_999_999)
    response = api_session.get(f"{base_url}/pet/{missing_id}")
    assert response.status_code == 404
    body = response.json()
    assert body["code"] == 1
    assert body["message"] == "Pet not found"


def test_delete_nonexistent_pet_returns_404(api_session, base_url):
    missing_id = random.randint(9_000_000_000, 9_999_999_999)
    response = api_session.delete(f"{base_url}/pet/{missing_id}")
    assert response.status_code == 404


def test_create_pet_with_invalid_body_returns_400(api_session, base_url):
    headers = {"Content-Type": "application/json"}
    response = api_session.post(f"{base_url}/pet", data="not valid json", headers=headers)
    assert response.status_code == 400
    body = response.json()
    assert body["code"] == 400
    assert "bad input" in body["message"].lower()


def test_update_pet_with_wrong_content_type_returns_415(api_session, base_url):
    headers = {"Content-Type": "text/plain"}
    payload = '{"id": 1}'
    response = api_session.put(f"{base_url}/pet", data=payload, headers=headers)
    assert response.status_code == 415
    assert "xml" in response.headers.get("Content-Type", "").lower()
