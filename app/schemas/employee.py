from pydantic import BaseModel, ConfigDict
from app.schemas.departments import DepartmentResponse

class EmployeeCreate(BaseModel):
    fullname: str
    position: str
    department_id: int


class EmployeeResponse(BaseModel):
    id: int
    fullname: str
    position: str
    department: DepartmentResponse

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdate(BaseModel):
    fullname: str | None = None
    position: str | None = None
    department_id: int | None = None