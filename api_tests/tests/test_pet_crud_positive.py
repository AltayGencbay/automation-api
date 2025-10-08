import random
import string
import time
from typing import Dict
from urllib.parse import urljoin

from requests import Session

import pytest


def random_name(prefix: str = "pet") -> str:
    suffix = "".join(random.choices(string.ascii_lowercase, k=6))
    return f"{prefix}-{suffix}"


def build_pet_payload() -> Dict:
    pet_id = random.randint(1_000_000, 9_999_999)
    return {
        "id": pet_id,
        "category": {"id": pet_id, "name": "cats"},
        "name": random_name(),
        "photoUrls": ["https://example.com/photo1.jpg"],
        "tags": [{"id": pet_id, "name": "test"}],
        "status": "available",
    }


def fetch_pet_with_retry(session: Session, base_url: str, pet_id: int, attempts: int = 5, delay: float = 0.3):
    response = None
    pet_url = urljoin(f"{base_url}/", f"pet/{pet_id}")
    for _ in range(attempts):
        response = session.get(pet_url)
        if response.status_code == 200:
            return response
        time.sleep(delay)
    return response


def delete_pet_with_retry(session: Session, base_url: str, pet_id: int, attempts: int = 5, delay: float = 0.3):
    response = None
    pet_url = urljoin(f"{base_url}/", f"pet/{pet_id}")
    for _ in range(attempts):
        response = session.delete(pet_url)
        if response.status_code == 200:
            return response
        time.sleep(delay)
    return response


@pytest.mark.usefixtures("api_session", "assert_pet_schema")
class TestPetCrudPositive:
    def test_create_pet_success(self, api_session, base_url, assert_pet_schema):
        payload = build_pet_payload()
        response = api_session.post(f"{base_url}/pet", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == payload["id"]
        assert data["name"] == payload["name"]
        assert data["status"] == payload["status"]
        assert_pet_schema(data)

        delete_pet_with_retry(api_session, base_url, payload["id"])

    def test_get_pet_success(self, api_session, base_url, assert_pet_schema):
        payload = build_pet_payload()
        create_resp = api_session.post(f"{base_url}/pet", json=payload)
        create_resp.raise_for_status()

        get_resp = fetch_pet_with_retry(api_session, base_url, payload["id"])
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["id"] == payload["id"]
        assert data["name"] == payload["name"]
        assert data["status"] == payload["status"]
        assert_pet_schema(data)

        delete_pet_with_retry(api_session, base_url, payload["id"])

    def test_update_pet_success(self, api_session, base_url, assert_pet_schema):
        payload = build_pet_payload()
        create_resp = api_session.post(f"{base_url}/pet", json=payload)
        create_resp.raise_for_status()

        updated_payload = {
            **payload,
            "name": random_name("updated"),
            "status": "pending",
        }
        update_resp = api_session.put(f"{base_url}/pet", json=updated_payload)
        assert update_resp.status_code == 200
        updated_data = update_resp.json()
        assert updated_data["name"] == updated_payload["name"]
        assert updated_data["status"] == updated_payload["status"]
        assert_pet_schema(updated_data)

        delete_pet_with_retry(api_session, base_url, payload["id"])

    def test_delete_pet_success(self, api_session, base_url):
        payload = build_pet_payload()
        create_resp = api_session.post(f"{base_url}/pet", json=payload)
        create_resp.raise_for_status()

        fetch_resp = fetch_pet_with_retry(api_session, base_url, payload["id"])
        assert fetch_resp.status_code == 200

        delete_resp = delete_pet_with_retry(api_session, base_url, payload["id"])
        assert delete_resp.status_code == 200

        time.sleep(0.3)
        get_resp = api_session.get(f"{base_url}/pet/{payload['id']}")
        assert get_resp.status_code == 404
