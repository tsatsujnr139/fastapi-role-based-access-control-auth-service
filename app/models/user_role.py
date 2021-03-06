from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class UserRole(Base):
    __tablename__ = "user_roles"
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id"),
        primary_key=True,
        nullable=False,
    )

    role = relationship("Role")
    user = relationship("User", back_populates="user_role", uselist=False)

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="unique_user_role"),
    )
