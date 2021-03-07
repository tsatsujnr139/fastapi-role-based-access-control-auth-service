from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from fastapi import APIRouter, Body, Depends, HTTPException, Security
from pydantic.types import UUID4
from sqlalchemy.orm import Session

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=List[schemas.Account])
def get_accounts(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve all accounts.
    """
    accounts = crud.account.get_multi(db, skip=skip, limit=limit)
    return accounts


@router.get("/me", response_model=schemas.Account)
def get_account_for_user(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve account for a logged in user.
    """
    account = crud.account.get(db, id=current_user.account_id)
    return account


@router.post("", response_model=schemas.Account)
def create_account(
    *,
    db: Session = Depends(deps.get_db),
    account_in: schemas.AccountCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create an user account
    """
    account = crud.account.get_by_name(db, name=account_in.name)
    if account:
        raise HTTPException(
            status_code=409, detail="An account with this name already exists",
        )
    account = crud.account.create(db, obj_in=account_in)
    return account


@router.put("/{account_id}", response_model=schemas.Account)
def update_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: UUID4,
    account_in: schemas.AccountUpdate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ACCOUNT_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Update an account.
    """

    # If user is an account admin, check ensure they update their own account.
    if current_user.user_role.role.name == Role.ACCOUNT_ADMIN["name"]:
        if current_user.account_id != account_id:
            raise HTTPException(
                status_code=401,
                detail=(
                    "This user does not have the permissions to "
                    "update this account"
                ),
            )
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="Account does not exist",
        )
    account = crud.account.update(db, db_obj=account, obj_in=account_in)
    return account


@router.post("/{account_id}/users", response_model=schemas.User)
def add_user_to_account(
    *,
    db: Session = Depends(deps.get_db),
    account_id: UUID4,
    user_id: str = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a user to an account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="Account does not exist",
        )
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="User does not exist",
        )
    user_in = schemas.UserUpdate(account_id=account_id)
    updated_user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return updated_user


@router.get("/{account_id}/users", response_model=List[schemas.User])
def retrieve_users_for_account(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    account_id: UUID4,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[Role.ADMIN["name"], Role.SUPER_ADMIN["name"]],
    ),
) -> Any:
    """
    Retrieve users for an account.
    """
    account = crud.account.get(db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="Account does not exist",
        )
    account_users = crud.user.get_by_account_id(
        db, account_id=account_id, skip=skip, limit=limit
    )
    return account_users


@router.get("/users/me", response_model=List[schemas.Account])
def retrieve_users_for_own_account(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ACCOUNT_ADMIN["name"],
        ],
    ),
) -> Any:
    """
    Retrieve users for own account.
    """
    account = crud.account.get(db, id=current_user.account_id)
    if not account:
        raise HTTPException(
            status_code=404, detail="Account does not exist",
        )
    account_users = crud.user.get_by_account_id(
        db, account_id=account.id, skip=skip, limit=limit
    )
    return account_users
