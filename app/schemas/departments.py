
from pydantic import BaseModel, ConfigDict

class DepartmentCreate(BaseModel):
    name: str


class DepartmentResponse(BaseModel):
    id: int
    name: str


class DepartmentUpdate(BaseModel):
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)





