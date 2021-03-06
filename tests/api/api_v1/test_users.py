from typing import Dict

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.user import regular_user_email
from tests.utils.utils import random_email, random_lower_string


def test_get_own_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers
    )
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["email"] == regular_user_email


def test_create_user_by_superadmin(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    data = {"email": username, "password": password, "full_name": full_name}
    r = client.post(
        f"{settings.API_V1_STR}/users",
        headers=superadmin_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]


def test_create_user_by_normal_user_is_unauthorized(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    data = {"email": username, "password": password, "full_name": full_name}
    r = client.post(
        f"{settings.API_V1_STR}/users",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 401


def test_create_user_open(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    data = {"email": username, "password": password, "full_name": full_name}
    r = client.post(
        f"{settings.API_V1_STR}/users/open",
        headers=normal_user_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]


def test_get_existing_user_by_superadmin(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superadmin_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_for_normal_user_is_unauthorized(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 401


def test_create_user_existing_username(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    username = random_email()
    full_name = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(
        email=username, password=password, full_name=full_name
    )
    crud.user.create(db, obj_in=user_in)
    data = {"email": username, "password": password, "full_name": full_name}
    r = client.post(
        f"{settings.API_V1_STR}/users",
        headers=superadmin_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 409
    assert "_id" not in created_user


def test_create_user_open_existing_username(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    full_name = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(
        email=username, password=password, full_name=full_name
    )
    crud.user.create(db, obj_in=user_in)
    data = {"email": username, "password": password, "full_name": full_name}
    r = client.post(
        f"{settings.API_V1_STR}/users/open",
        headers=normal_user_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 409
    assert "_id" not in created_user


def test_retrieve_users_by_superadmin(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.user.create(db, obj_in=user_in2)

    r = client.get(
        f"{settings.API_V1_STR}/users/", headers=superadmin_token_headers
    )
    all_users = r.json()
    assert len(all_users) > 1


def test_retrieve_users_by_normal_user_is_unauthorized(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.user.create(db, obj_in=user_in2)

    r = client.get(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers
    )
    assert r.status_code == 401
