from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey

from app.models.base import Base
from app.models.mixins import TimeStampMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from app.models.employee import Employee


class Request(Base, TimeStampMixin):
    __tablename__ = "requests"

    number: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=False)
    deadline: Mapped[datetime]  = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    executor_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))

    author: Mapped["Employee"] = relationship("Employee",
                          back_populates="created_requests",
                          foreign_keys=[author_id])
    executor: Mapped["Employee"] = relationship("Employee",
                            back_populates="assigned_requests",
                            foreign_keys=[executor_id])
