from typing import Dict

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

regular_user_email = "tester@email.com"
regular_user_password = "supersecretpassword"
regular_user_full_name = "john doe"


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/auth/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_superadmin_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPER_ADMIN_EMAIL,
        "password": settings.FIRST_SUPER_ADMIN_PASSWORD,
    }
    r = client.post(
        f"{settings.API_V1_STR}/auth/access-token", data=login_data
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(
            username=email,
            email=email,
            full_name=regular_user_full_name,
            password=regular_user_password,
        )
        user = crud.user.create(db, obj_in=user_in_create)

    return user_authentication_headers(
        client=client, email=email, password=regular_user_password
    )
