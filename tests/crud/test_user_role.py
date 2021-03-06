from app import crud, schemas
from sqlalchemy.orm import Session
from tests.utils.utils import random_email, random_lower_string


def test_create_user_role(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    role = crud.role.get_by_name(db, name="ACCOUNT_ADMIN")
    user_role_in = schemas.UserRoleCreate(user_id=user.id, role_id=role.id)
    user_role = crud.user_role.create(db, obj_in=user_role_in)
    assert user_role.user_id == user.id
    assert user_role.role_id == role.id


def test_get_user_role_by_user_id(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    role = crud.role.get_by_name(db, name="ACCOUNT_ADMIN")
    user_role_in = schemas.UserRoleCreate(user_id=user.id, role_id=role.id)
    user_role = crud.user_role.create(db, obj_in=user_role_in)
    user_role_2 = crud.user_role.get_by_user_id(db, user_id=user.id)
    assert user_role.user_id == user_role_2.user_id


def test_update_user_role(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    role = crud.role.get_by_name(db, name="ACCOUNT_ADMIN")
    user_role_in = schemas.UserRoleCreate(user_id=user.id, role_id=role.id)
    user_role = crud.user_role.create(db, obj_in=user_role_in)
    new_role = crud.role.get_by_name(db, name="ACCOUNT_MANAGER")
    new_user_role_in = schemas.UserRoleUpdate(role_id=new_role.id)
    new_user_role = crud.user_role.update(
        db, db_obj=user_role, obj_in=new_user_role_in
    )
    assert new_user_role.role_id == new_role.id
