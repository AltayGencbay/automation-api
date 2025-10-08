import json
from pathlib import Path
from typing import Any, Callable, Dict

import pytest
import requests
from jsonschema import Draft7Validator

from utils.logger import get_logger


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://petstore.swagger.io/v2"


@pytest.fixture(scope="session")
def pet_schema_validator() -> Draft7Validator:
    schema_path = Path(__file__).parent / "schemas" / "pet_schema.json"
    with schema_path.open("r", encoding="utf-8") as schema_file:
        schema = json.load(schema_file)
    return Draft7Validator(schema)


@pytest.fixture
def api_session() -> requests.Session:
    logger = get_logger("api_tests.session")
    session = requests.Session()

    def log_response(response: requests.Response, *args: Any, **kwargs: Any) -> None:
        request = response.request

        def safe_body(data: Any) -> str:
            if data is None:
                return ""
            if isinstance(data, (bytes, bytearray)):
                return data.decode("utf-8", errors="replace")
            return str(data)

        logger.info(
            "Request: %s %s | Body: %s",
            request.method,
            request.url,
            safe_body(request.body),
        )
        logger.info(
            "Response: %s %s | Status: %s | Body: %s",
            request.method,
            response.url,
            response.status_code,
            safe_body(response.text),
        )

    session.hooks["response"] = [log_response]
    yield session
    session.close()


@pytest.fixture
def assert_pet_schema(pet_schema_validator: Draft7Validator) -> Callable[[Dict[str, Any]], None]:
    def _assert(payload: Dict[str, Any]) -> None:
        errors = sorted(pet_schema_validator.iter_errors(payload), key=lambda e: e.path)
        assert not errors, f"Schema validation errors: {[error.message for error in errors]}"

    return _assert
