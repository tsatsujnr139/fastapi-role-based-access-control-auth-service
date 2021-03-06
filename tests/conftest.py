from typing import Dict, Generator

import pytest
from app.api.deps import get_db
from app.db.session import TestingSessionLocal
from app.main import app
from fastapi.testclient import TestClient

from tests.utils.user import (
    authentication_token_from_email,
    get_superadmin_token_headers,
    regular_user_email,
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superadmin_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superadmin_token_headers(client=client)


@pytest.fixture(scope="module")
def normal_user_token_headers(
    client: TestClient, db: TestingSessionLocal
) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=regular_user_email, db=db
    )
