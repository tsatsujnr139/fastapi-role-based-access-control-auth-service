from typing import Optional

from pydantic import UUID4, BaseModel


# Shared properties
class RoleBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    pass


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: UUID4

    class Config:
        orm_mode = True


# Additional properties to return via API
class Role(RoleInDBBase):
    pass


class RoleInDB(RoleInDBBase):
    pass
