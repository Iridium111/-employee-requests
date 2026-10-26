import uuid
from sqlalchemy import ForeignKey

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from app.models.employee import Employee

class User(Base):
    __tablename__="users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(nullable=True, default=None)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), unique=True)

    employee: Mapped["Employee"] = relationship("Employee", back_populates="user")