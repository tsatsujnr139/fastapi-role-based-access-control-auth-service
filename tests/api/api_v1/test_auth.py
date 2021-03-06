from typing import Dict

from app.core.config import settings
from fastapi.testclient import TestClient
from tests.utils.user import regular_user_email, regular_user_password


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": regular_user_email,
        "password": regular_user_password,
    }
    r = client.post(
        f"{settings.API_V1_STR}/auth/access-token", data=login_data
    )
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/auth/test-token",
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
