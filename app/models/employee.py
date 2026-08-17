from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.request import Request


class Employee(Base):
    __tablename__ = "employees"

    fullname: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[str] = mapped_column(nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))

    department = relationship("Department", back_populates="employees")
    created_requests: Mapped[list[Request]] = relationship("Request",
                                                           back_populates="author",
                                                           foreign_keys="Request.author_id")
    assigned_requests: Mapped[list[Request]] = relationship("Request",
                                                            back_populates="executor",
                                                            foreign_keys="Request.executor_id")