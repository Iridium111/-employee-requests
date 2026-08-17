from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.employee import Employee


class Department(Base):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(nullable=False)

    employees: Mapped[list[Employee]] = relationship("Employee", back_populates="department")