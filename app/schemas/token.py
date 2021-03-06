from pydantic import UUID4, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    id: UUID4
    role: str = None
    account_id: UUID4 = None
