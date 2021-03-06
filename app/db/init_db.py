from app import crud, schemas
from app.constants.role import Role
from app.core.config import settings
from sqlalchemy.orm import Session


def init_db(db: Session) -> None:

    # Create Super Admin Account
    account = crud.account.get_by_name(
        db, name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME
    )
    if not account:
        account_in = schemas.AccountCreate(
            name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME,
            description="superadmin account",
        )
        crud.account.create(db, obj_in=account_in)

    # Create 1st Superuser
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPER_ADMIN_EMAIL)
    if not user:
        account = crud.account.get_by_name(
            db, name=settings.FIRST_SUPER_ADMIN_ACCOUNT_NAME
        )
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPER_ADMIN_EMAIL,
            password=settings.FIRST_SUPER_ADMIN_PASSWORD,
            full_name=settings.FIRST_SUPER_ADMIN_EMAIL,
            account_id=account.id,
        )
        user = crud.user.create(db, obj_in=user_in)

    # Create Role If They Don't Exist
    guest_role = crud.role.get_by_name(db, name=Role.GUEST["name"])
    if not guest_role:
        guest_role_in = schemas.RoleCreate(
            name=Role.GUEST["name"], description=Role.GUEST["description"]
        )
        crud.role.create(db, obj_in=guest_role_in)

    account_admin_role = crud.role.get_by_name(
        db, name=Role.ACCOUNT_ADMIN["name"]
    )
    if not account_admin_role:
        account_admin_role_in = schemas.RoleCreate(
            name=Role.ACCOUNT_ADMIN["name"],
            description=Role.ACCOUNT_ADMIN["description"],
        )
        crud.role.create(db, obj_in=account_admin_role_in)

    account_manager_role = crud.role.get_by_name(
        db, name=Role.ACCOUNT_MANAGER["name"]
    )
    if not account_manager_role:
        account_manager_role_in = schemas.RoleCreate(
            name=Role.ACCOUNT_MANAGER["name"],
            description=Role.ACCOUNT_MANAGER["description"],
        )
        crud.role.create(db, obj_in=account_manager_role_in)

    admin_role = crud.role.get_by_name(db, name=Role.ADMIN["name"])
    if not admin_role:
        admin_role_in = schemas.RoleCreate(
            name=Role.ADMIN["name"], description=Role.ADMIN["description"]
        )
        crud.role.create(db, obj_in=admin_role_in)

    super_admin_role = crud.role.get_by_name(db, name=Role.SUPER_ADMIN["name"])
    if not super_admin_role:
        super_admin_role_in = schemas.RoleCreate(
            name=Role.SUPER_ADMIN["name"],
            description=Role.SUPER_ADMIN["description"],
        )
        crud.role.create(db, obj_in=super_admin_role_in)

    # Assign super_admin role to user
    user_role = crud.user_role.get_by_user_id(db, user_id=user.id)
    if not user_role:
        role = crud.role.get_by_name(db, name=Role.SUPER_ADMIN["name"])
        user_role_in = schemas.UserRoleCreate(user_id=user.id, role_id=role.id)
        crud.user_role.create(db, obj_in=user_role_in)
