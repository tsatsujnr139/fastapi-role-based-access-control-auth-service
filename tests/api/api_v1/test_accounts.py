from app import crud, schemas
from app.core.config import settings
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.utils.user import regular_user_email
from tests.utils.utils import random_email, random_lower_string


def test_create_account(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    data = {"name": account_name, "description": account_description}
    r = client.post(
        f"{settings.API_V1_STR}/accounts",
        headers=superadmin_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_account = r.json()
    account = crud.account.get_by_name(db, name=account_name)
    assert account
    assert account.name == created_account["name"]


def test_update_account(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = crud.account.create(db, obj_in=account_in)
    new_account_name = random_lower_string()
    data = {"name": new_account_name}
    r = client.put(
        f"{settings.API_V1_STR}/accounts/{account.id}",
        headers=superadmin_token_headers,
        json=data,
    )
    updated_account = r.json()
    assert 200 <= r.status_code < 300
    assert updated_account["name"] == new_account_name


def test_add_user_to_account(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = crud.account.create(db, obj_in=account_in)
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPER_ADMIN_EMAIL)
    data = {"user_id": str(user.id)}
    r = client.post(
        f"{settings.API_V1_STR}/accounts/{str(account.id)}/users",
        headers=superadmin_token_headers,
        json=data,
    )
    user = r.json()
    assert 200 <= r.status_code < 300
    assert user["account_id"] == str(account.id)


def test_get_all_accounts_by_authorised_user(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account_name_2 = random_lower_string()
    account_description_2 = random_lower_string()
    account_in_2 = schemas.AccountCreate(
        name=account_name_2, description=account_description_2
    )
    crud.account.create(db, obj_in=account_in)
    crud.account.create(db, obj_in=account_in_2)
    r = client.get(
        f"{settings.API_V1_STR}/accounts", headers=superadmin_token_headers
    )
    assert 200 <= r.status_code < 300


def test_get_all_accounts_by_uauthorised_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account_name_2 = random_lower_string()
    account_description_2 = random_lower_string()
    account_in_2 = schemas.AccountCreate(
        name=account_name_2, description=account_description_2
    )
    crud.account.create(db, obj_in=account_in)
    crud.account.create(db, obj_in=account_in_2)
    r = client.get(
        f"{settings.API_V1_STR}/accounts", headers=normal_user_token_headers
    )
    assert r.status_code == 401


def test_get_account_for_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = crud.account.create(db, obj_in=account_in)
    user = crud.user.get_by_email(db, email=regular_user_email)
    user_update_in = schemas.UserUpdate(account_id=account.id)
    crud.user.update(db, db_obj=user, obj_in=user_update_in)
    r = client.get(
        f"{settings.API_V1_STR}/accounts/me", headers=normal_user_token_headers
    )
    user_account = r.json()
    print(account)
    assert 200 <= r.status_code < 300
    assert user_account["id"] == str(account.id)


def test_get_users_for_account_by_authorized_user(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = crud.account.create(db, obj_in=account_in)
    user_in = schemas.UserCreate(
        email=random_email(),
        full_name=random_lower_string(),
        password=random_lower_string(),
        account_id=account.id,
    )
    user_in_2 = schemas.UserCreate(
        email=random_email(),
        full_name=random_lower_string(),
        password=random_lower_string(),
        account_id=account.id,
    )
    crud.user.create(db, obj_in=user_in)
    crud.user.create(db, obj_in=user_in_2)
    r = client.get(
        f"{settings.API_V1_STR}/accounts/{str(account.id)}/users",
        headers=superadmin_token_headers,
    )
    users = r.json()
    assert 200 <= r.status_code < 300
    assert len(users) == 2


def test_get_users_for_account_by_unauthorized_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    account_name = random_lower_string()
    account_description = random_lower_string()
    account_in = schemas.AccountCreate(
        name=account_name, description=account_description
    )
    account = crud.account.create(db, obj_in=account_in)
    r = client.get(
        f"{settings.API_V1_STR}/accounts/{str(account.id)}/users",
        headers=normal_user_token_headers,
    )

    assert r.status_code == 401


def test_get_users_for_own_account(
    client: TestClient, superadmin_token_headers: dict, db: Session
) -> None:
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPER_ADMIN_EMAIL)
    user_in = schemas.UserCreate(
        email=random_email(),
        full_name=random_lower_string(),
        password=random_lower_string(),
        account_id=user.account_id,
    )
    user_in_2 = schemas.UserCreate(
        email=random_email(),
        full_name=random_lower_string(),
        password=random_lower_string(),
        account_id=user.account_id,
    )
    crud.user.create(db, obj_in=user_in)
    crud.user.create(db, obj_in=user_in_2)
    r = client.get(
        f"{settings.API_V1_STR}/accounts/users/me",
        headers=superadmin_token_headers,
    )
    assert 200 <= r.status_code < 300
