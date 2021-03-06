from app import crud
from app.constants.role import Role
from app.core.config import settings
from app.schemas.user import UserCreate
from app.schemas.user_role import UserRoleCreate
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.utils import random_email, random_lower_string


def test_assign_user_role_by_superadmin(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    user_in = UserCreate(
        email=username, password=password, full_name=full_name
    )
    user = crud.user.create(db, obj_in=user_in)
    role = crud.role.get_by_name(db, name=Role.ACCOUNT_MANAGER["name"])
    data = {"user_id": str(user.id), "role_id": str(role.id)}
    r = client.post(
        f"{settings.API_V1_STR}/user-roles",
        headers=superadmin_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user_role = r.json()
    user_role = crud.user_role.get_by_user_id(db, user_id=user.id)
    assert user_role
    assert str(user_role.role_id) == created_user_role["role_id"]


def test_assign_user_role_by_normal_user(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    user_in = UserCreate(
        email=username, password=password, full_name=full_name
    )
    user = crud.user.create(db, obj_in=user_in)
    role = crud.role.get_by_name(db, name=Role.ACCOUNT_MANAGER["name"])
    data = {"user_id": str(user.id), "role_id": str(role.id)}
    r = client.post(
        f"{settings.API_V1_STR}/user-roles",
        headers=superadmin_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user_role = r.json()
    user_role = crud.user_role.get_by_user_id(db, user_id=user.id)
    assert user_role
    assert str(user_role.role_id) == created_user_role["role_id"]


def test_update_user_role(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    user_in = UserCreate(
        email=username, password=password, full_name=full_name
    )
    user = crud.user.create(db, obj_in=user_in)
    role = crud.role.get_by_name(db, name=Role.ACCOUNT_MANAGER["name"])
    user_role_in = UserRoleCreate(user_id=user.id, role_id=role.id)
    crud.user_role.create(db, obj_in=user_role_in)
    new_role = crud.role.get_by_name(db, name=Role.ACCOUNT_ADMIN["name"])
    data = {"role_id": str(new_role.id)}
    r = client.put(
        f"{settings.API_V1_STR}/user-roles/{user.id}",
        headers=superadmin_token_headers,
        json=data,
    )
    updated_user_role = r.json()
    assert 200 <= r.status_code < 300
    assert updated_user_role["role_id"] == str(new_role.id)


def test_update_user_role_by_unauthorized_user_fails(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    user_in = UserCreate(
        email=username, password=password, full_name=full_name
    )
    user = crud.user.create(db, obj_in=user_in)
    role = crud.role.get_by_name(db, name=Role.ACCOUNT_MANAGER["name"])
    user_role_in = UserRoleCreate(user_id=user.id, role_id=role.id)
    crud.user_role.create(db, obj_in=user_role_in)
    new_role = crud.role.get_by_name(db, name=Role.ACCOUNT_ADMIN["name"])
    data = {"role_id": str(new_role.id)}
    r = client.put(
        f"{settings.API_V1_STR}/user-roles/{user.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 401
